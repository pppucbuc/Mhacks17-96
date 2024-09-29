import React, { useState, StrictMode } from 'react';
import { createRoot } from "react-dom/client";
import SearchComponent from './Search';


// Create a root
const root = createRoot(document.getElementById("reactEntry"));

// This method is only called once
// Insert the post component into the DOM
root.render(
      <SearchComponent />
);