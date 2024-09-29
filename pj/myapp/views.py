from django.shortcuts import render
from django.http import JsonResponse
import heapq
from collections import defaultdict
import os
from pathlib import Path
import json
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from .Api import gpt_request 

# Helper function: calculate averages with fallback
def calculate_avg_with_fallback(hw_scores, quiz_scores, exam_scores):
    # hw_scores = [float(score) for score in hw_scores if isinstance(score, (int, float, str)) and str(score).replace('.', '', 1).isdigit()]
    # quiz_scores = [float(score) for score in quiz_scores if isinstance(score, (int, float, str)) and str(score).replace('.', '', 1).isdigit()]
    # exam_scores = [float(score) for score in exam_scores if isinstance(score, (int, float, str)) and str(score).replace('.', '', 1).isdigit()]
    hw_avg = np.mean(hw_scores) if len(hw_scores) > 0 else None
    quiz_avg = np.mean(quiz_scores) if len(quiz_scores) > 0 else None
    exam_avg = np.mean(exam_scores) if len(exam_scores) > 0 else None

    # If any category is missing, take the average of the other non-empty ones
    if hw_avg is None:
        hw_avg = np.mean([avg for avg in [quiz_avg, exam_avg] if avg is not None])
        hw_scores.append(np.mean([avg for avg in [quiz_avg, exam_avg] if avg is not None]))
    if quiz_avg is None:
        quiz_avg = np.mean([avg for avg in [hw_avg, exam_avg] if avg is not None])
        quiz_scores.append(np.mean([avg for avg in [hw_avg, exam_avg] if avg is not None]))
    if exam_avg is None:
        exam_avg = np.mean([avg for avg in [hw_avg, quiz_avg] if avg is not None])
        exam_scores.append(np.mean([avg for avg in [hw_avg, quiz_avg] if avg is not None]))

    return hw_avg, quiz_avg, exam_avg

# Weighted average function
def weighted_average(hw_avg, quiz_avg, exam_avg, hw_count, quiz_count, exam_count):
    total_count = hw_count + quiz_count + exam_count
    weights = {
        'HW': hw_count / total_count if total_count > 0 else 0,
        'Quiz': quiz_count / total_count if total_count > 0 else 0,
        'Exams': exam_count / total_count if total_count > 0 else 0
    }
    return (hw_avg * weights['HW'] +
            quiz_avg * weights['Quiz'] +
            exam_avg * weights['Exams'])

    # Evaluate grade from score
def evaluate_grade(score):
    if score >= 97:
        return 'A+'
    elif score >= 93:
        return 'A'
    elif score >= 90:
        return 'A-'
    elif score >= 87:
        return 'B+'
    elif score >= 83:
        return 'B'
    elif score >= 80:
        return 'B-'
    elif score >= 77:
        return 'C+'
    elif score >= 73:
        return 'C'
    elif score >= 70:
        return 'C-'
    elif score >= 67:
        return 'D+'
    elif score >= 63:
        return 'D'
    elif score >= 60:
        return 'D-'
    else:
        return 'F'

    # Simulate future scores function
def simulate_future_scores(current_final_score, hw_scores, quiz_scores, exam_scores, hw_count, quiz_count, exam_count, mode):
    future_scores = []  # Start with the current score
    simulated_this_score = []
    simulation_name=[]

    # Ensure copies to avoid modifying original lists
    hw_scores = hw_scores.copy()
    quiz_scores = quiz_scores.copy()
    exam_scores = exam_scores.copy()

    # Get current counts
    current_hw_count = len(hw_scores)
    current_quiz_count = len(quiz_scores)
    current_exam_count = len(exam_scores)

    # Calculate current averages
    hw_avg = np.mean(hw_scores) if current_hw_count > 0 else 0
    quiz_avg = np.mean(quiz_scores) if current_quiz_count > 0 else 0
    exam_avg = np.mean(exam_scores) if current_exam_count > 0 else 0

    # Simulate future homework scores
    for _ in range(hw_count - current_hw_count):
        if mode == 'trend':
            predicted_hw_score = np.clip(np.random.normal(loc=hw_avg, scale=1), 0, 100)
        elif mode == 'improve':
            predicted_hw_score = np.clip(np.random.normal(loc=hw_avg + 1, scale=2), 0, 100)
        elif mode == 'regress':
            predicted_hw_score = np.clip(np.random.normal(loc=hw_avg - 1, scale=2), 0, 100)

        # Append new scores and recalculate averages
        hw_scores.append(predicted_hw_score)
        current_hw_count += 1
        hw_avg = np.mean(hw_scores)

        final_score = weighted_average(
            hw_avg,
            quiz_avg,
            exam_avg,
            current_hw_count,
            current_quiz_count,
            current_exam_count
        )
        future_scores.append(final_score)
        simulated_this_score.append(predicted_hw_score)
        simulation_name.append(f"HW{current_hw_count}")

    # Simulate future quiz scores
    for _ in range(quiz_count - current_quiz_count):
        if mode == 'trend':
            predicted_quiz_score = np.clip(np.random.normal(loc=quiz_avg, scale=1), 0, 100)
        elif mode == 'improve':
            predicted_quiz_score = np.clip(np.random.normal(loc=quiz_avg + 1, scale=2), 0, 100)
        elif mode == 'regress':
            predicted_quiz_score = np.clip(np.random.normal(loc=quiz_avg - 1, scale=2), 0, 100)

        # Append new scores and recalculate averages
        quiz_scores.append(predicted_quiz_score)
        current_quiz_count += 1
        quiz_avg = np.mean(quiz_scores)

        final_score = weighted_average(
            hw_avg,
            quiz_avg,
            exam_avg,
            current_hw_count,
            current_quiz_count,
            current_exam_count
        )
        future_scores.append(final_score)
        simulated_this_score.append(predicted_quiz_score)
        simulation_name.append(f"Quiz{current_quiz_count}")

    # Simulate future exam scores
    for _ in range(exam_count - current_exam_count):
        if mode == 'trend':
            predicted_exam_score = np.clip(np.random.normal(loc=exam_avg, scale=1), 0, 100)
        elif mode == 'improve':
            predicted_exam_score = np.clip(np.random.normal(loc=exam_avg + 1, scale=2), 0, 100)
        elif mode == 'regress':
            predicted_exam_score = np.clip(np.random.normal(loc=exam_avg - 1, scale=2), 0, 100)

        # Append new scores and recalculate averages
        exam_scores.append(predicted_exam_score)
        current_exam_count += 1
        exam_avg = np.mean(exam_scores)

        final_score = weighted_average(
            hw_avg,
            quiz_avg,
            exam_avg,
            current_hw_count,
            current_quiz_count,
            current_exam_count
        )
        future_scores.append(final_score)
        simulated_this_score.append(predicted_exam_score)
        simulation_name.append(f"Exam{current_exam_count}")

    return future_scores,  simulated_this_score, simulation_name


def index(request):
    context = {
        'message': 'Welcome to the home page!',
    }
    return render(request, 'base.html', context)
# Create your views here.
@csrf_exempt
def calculate(request):
    data = json.loads(request.body)
    destination_query = data.get('destinationQuery')
    Grades_ = data.get('grades')
    print(type(Grades_))

    data = {
        'student_id': [1],  # Only one student
        'HW_scores': [[]],  # Empty HW scores for testing
        'Quiz_scores': [[]], # Placeholder for Quiz scores
        'Exam_scores': [[]]  # Empty exam scores for testing
    }

    for item in Grades_:
        if item['type'] == 'Quiz':
            data['Quiz_scores'][0] = [int(num) for num in item['grades'] if num] # Add quiz scores
        elif item['type'] == 'Exam':
            data['Exam_scores'][0] =  [int(num) for num in item['grades'] if num]  # Add exam scores
        elif item['type'] == 'Assignment':
            data['HW_scores'][0] =  [int(num) for num in item['grades'] if num]
    
    # print(type(data['Quiz_scores'][0][0]))
   

    # data = {
    # 'student_id': [1],  # Only one student
    # 'HW_scores': [[86, 87, 85]],  # Homework scores
    # 'Quiz_scores': [[87, 90]],     # Quiz scores
    # 'Exam_scores': [[]],      # Empty exam scores for testing
# }
    # print(type(data['Quiz_scores'][0][0]))
    df = pd.DataFrame(data)

    # Main Workflow_____________________________________________________________________________________________________________________________________________#

    # Extract the scores
    hw_scores = list(df['HW_scores'][0])
    quiz_scores = list(df['Quiz_scores'][0])
    exam_scores = list(df['Exam_scores'][0])

    # Define total future assessments to simulate
    total_hw = 5
    total_quiz = 3
    total_exam = 2

    # Simulate scores for different modes
    modes = ['trend', 'improve', 'regress']

    # Calculate averages, handling empty categories
    hw_avg, quiz_avg, exam_avg = calculate_avg_with_fallback(hw_scores, quiz_scores, exam_scores)

    # Current final score calculation
    if hw_avg is not None and quiz_avg is not None and exam_avg is not None:
        current_final_score = weighted_average(hw_avg, quiz_avg, exam_avg, len(hw_scores), len(quiz_scores), len(exam_scores))

        future_scores_all_modes = {
            mode: simulate_future_scores(
                current_final_score,
                hw_scores,
                quiz_scores,
                exam_scores,
                total_hw,
                total_quiz,
                total_exam,
                mode
            ) for mode in modes
        }
        output_lines = []
        # Output results and plot the score trends
        for mode, (scores, simulated_this_score, simulation_name) in future_scores_all_modes.items():
            if(mode == 'trend'):
                output_lines.append(f"If you pay the same effort as previous work,")
                print((f"If you worker than before,"))
            if(mode == 'regress'):
                output_lines.append(f"If you become lazy,")
                print((f"If you worker than before,")  )
            if(mode == 'improve'):
                output_lines.append(f"If you worker than before,")        
                print((f"If you worker than before,")  )    
            for i, score in enumerate(scores):
                simulated_score = int(simulated_this_score[i]) if i < len(simulated_this_score) else "N/A"
                name = simulation_name[i]   if i < len(simulation_name) else "N/A"
                output_lines.append(f"Your {name} will probably be {simulated_score}, and the final score will be: {score:.2f}({evaluate_grade(score)}) ")
                print(f"Your {name} will probably be {simulated_score}, and the final score will be: {score:.2f}({evaluate_grade(score)}) ")
        output_result = "\n".join(output_lines)
        # Create meaningful x-axis labels for future simulations
        # labels = []
        # for i in range(1, total_hw + 1):
        #     labels.append(f"HW{i+len(hw_scores)}")
        # for i in range(1, total_quiz + 1):
        #     labels.append(f"Quiz{i+len(quiz_scores)}")
        # for i in range(1, total_exam + 1):
        #     labels.append(f"Exam{i+len(exam_scores)}")

        # Plotting the score trends
        # plt.figure(figsize=(10, 6))
        # for mode, (scores, _, __) in future_scores_all_modes.items():
        #     plt.plot(scores, label=f'Predicted Scores - {mode}', marker='o')
        
        # plt.axhline(y=current_final_score, color='r', linestyle='--', label='Current Overall Score')
        # plt.title('Future Score Simulation with Individual Predictions')
        # plt.xlabel('Simulation Round')
        # plt.ylabel('Predicted Scores')

        # # Set x-axis labels
        # max_length = max(len(scores) for scores, _, __ in future_scores_all_modes.values())
        # full_labels = ['Start'] + labels[:max_length-1]  # Add the "Start" for the current score point
        # plt.xticks(range(max_length), full_labels, rotation=45)

        # plt.legend()
        # plt.grid()
        # plt.tight_layout()
        # plt.show()

    else:
        print("Invalid data. Cannot proceed with calculations.")

    response = gpt_request(output_result, destination_query)

    return JsonResponse({'response': response}, status=200)

