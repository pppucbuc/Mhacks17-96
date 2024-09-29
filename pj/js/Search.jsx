import React, { useState } from 'react';

const SearchComponent = () => {
  const [startQuery, setStartQuery] = useState('');
  const [destinationQuery, setDestinationQuery] = useState('');
  const [forms, setForms] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [newItemWeight, setNewItemWeight] = useState('');
  const [fetchedResults, setFetchedResults] = useState([]); // State for fetched data
  const itemTypes = ['Quiz', 'Assignment', 'Exam', 'Participation', 'Project'];

  const addForm = () => {
    setShowModal(true);
  };

  const handleSearch = (event) => {
    event.preventDefault();

    // Gather all submission data
    const submissionData = {
      startQuery,
      destinationQuery,
      grades: forms,
    };
    fetch('/api/calculate/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(submissionData),
    })
      .then(response => response.json())
      .then(data => {
        console.log(data);
        setFetchedResults(data.response); // Store fetched results in state
      })
      .catch(error => {
        console.error('Error:', error);
      });

    console.log('Submission Data:', submissionData);
  };

  const handleAddItem = (type) => {
    const weightValue = parseFloat(newItemWeight);
    if (!isNaN(weightValue)) {
      setForms([...forms, { type, weight: weightValue, grades: [] }]);
      setShowModal(false);
      setNewItemWeight('');
    } else {
      alert('Please enter a valid weight.');
    }
  };

  const addGradeField = (index) => {
    const updatedForms = [...forms];
    updatedForms[index].grades.push('');
    setForms(updatedForms);
  };

  const handleGradeChange = (itemIndex, gradeIndex, value) => {
    const updatedForms = [...forms];
    updatedForms[itemIndex].grades[gradeIndex] = value;
    setForms(updatedForms);
  };

  const deleteItem = (index) => {
    const updatedForms = forms.filter((_, i) => i !== index);
    setForms(updatedForms);
  };

  const deleteGradeField = (itemIndex, gradeIndex) => {
    const updatedForms = [...forms];
    updatedForms[itemIndex].grades.splice(gradeIndex, 1);
    setForms(updatedForms);
  };

  return (
    <div className="body_grade">
      <div class = 'center'>
        123123
      </div>
      <div>
        <button onClick={addForm} className="cute-button">Add New Item</button>
        {forms.map((form, itemIndex) => (
          <div key={itemIndex} className="grade-form">
            <div>Item Type: {form.type}</div>
            <div>Weight: {form.weight}</div>
            <button onClick={() => addGradeField(itemIndex)} className="add-grade-button">Add Grade</button>
            {form.grades.map((grade, gradeIndex) => (
              <div key={gradeIndex} className="grade-input">
                <input
                  type="text"
                  value={grade}
                  onChange={(e) => handleGradeChange(itemIndex, gradeIndex, e.target.value)}
                  placeholder={`${form.type} Grade ${gradeIndex + 1}`}
                />
                <button onClick={() => deleteGradeField(itemIndex, gradeIndex)} className="delete-grade-button">-</button>
              </div>
            ))}
            <button onClick={() => deleteItem(itemIndex)} className="delete-button">Delete Item</button>
          </div>
        ))}
      </div>

      {showModal && (
        <div className="modal">
          <div className="modal-content">
            <h2>Select Item Type</h2>
            {itemTypes.map((type) => (
              <button key={type} onClick={() => handleAddItem(type)} className="item-type-button">
                {type}
              </button>
            ))}
            <input
              type="number"
              value={newItemWeight}
              onChange={(e) => setNewItemWeight(e.target.value)}
              placeholder="Enter weight"
            />
            <button onClick={() => setShowModal(false)} className="close-button">Cancel</button>
          </div>
        </div>
      )}

      <form onSubmit={handleSearch}>
        <input
          type="text"
          value={destinationQuery}
          onChange={(e) => setDestinationQuery(e.target.value)}
          placeholder="Enter destination"
        />
        <button type="submit" className="cute-button">Submit</button>
      </form>

      {/* Display fetched results */}
      <div className="results">
        <h2>Academic Advisor:</h2>
        {fetchedResults ? ( // Check if fetchedResults is not an empty string
          <p>{fetchedResults}</p> // Display the string directly
        ) : (
          <p>No results to display.</p>
        )}
      </div>
    </div>
  );
};

export default SearchComponent;