import { useState } from "react";
import api from "../api"; // Assuming `api` is a configured Axios instance

const Generating = ({ className, onSubmit }) => {
  const [inputValue, setInputValue] = useState("");
  const [outputValue, setOutputValue] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Submitted: ", inputValue);

    try {
      const response = await api.post("/api/recommend/", { text: inputValue });
      if (response.status === 200) {
        setOutputValue(response.data.recommendation); // Assuming your backend returns a 'recommendation' field
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
    <div
      className={`flex items-center h-[3.5rem] px-6 bg-n-8/80 rounded-[1.7rem] ${
        className || ""
      } text-base`}
    >
      {/* Input field where users can click and type */}
      <input
        className="w-full h-full bg-transparent border-none text-white outline-none"
        type="text"
        placeholder="Enter movie description here"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)} // Update the state on typing
      />
      {/* Submit button to trigger submission */}
      <button
        className="ml-4 px-4 py-2 bg-purple-500 text-white rounded-full cursor-pointer"
        onClick={handleSubmit}
      >
        Submit
      </button>
      {outputValue && (
        <div className="ml-4 text-white">
          Recommendation: {outputValue}
        </div>
      )}
    </div>
  );
};

export default Generating;
