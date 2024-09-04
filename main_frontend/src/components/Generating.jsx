import { useState } from "react";
import api from "../api";

const Generating = ({ className, onSubmit }) => {
  const [inputValue, setInputValue] = useState("");
  const [outputValue, setOutputValue] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Submitted: ", inputValue);

    try {
      const response = await api.post("/api/recommend/", { text: inputValue });
      if (response.status === 200) {
        setOutputValue(response.data.recommendation); // Change to .recommendations if needed
      } else {
        console.error("Failed to get recommendation:", response.statusText);
      }
    } catch (error) {
      console.error("Error:", error);
    }

    // Optionally call the onSubmit prop if it is provided
    if (onSubmit) {
      onSubmit(inputValue);
    }
  };

  return (
    <div className={`flex flex-col items-center ${className || ""} text-base`}>
      {/* Input field and submit button */}
      <div className="flex items-center h-[3.5rem] px-6 bg-n-8/80 rounded-[1.7rem] text-base mb-4">
        <input
          className="w-full h-full bg-transparent border-none text-white outline-none"
          type="text"
          placeholder="Enter movie description here"
          id="textbox"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)} // Update the state on typing
        />
        <button
          className="ml-4 px-4 py-2 bg-purple-500 text-white rounded-full cursor-pointer"
          onClick={handleSubmit}
        >
          Submit
        </button>
      </div>

      {/* Separate area to display the output */}
      {outputValue && (
        <div className="mt-6 p-4 bg-gray-800 rounded-lg text-white max-w-2xl">
          <h3 className="text-lg font-semibold">Recommendation:</h3>
          <p>{outputValue}</p>
        </div>
      )}
    </div>
  );
};

export default Generating;
