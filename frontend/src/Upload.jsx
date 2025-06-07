import upload from '/Users/shabichasureshkumar/Desktop/shoplens/frontend/src/assets/upload.svg'
import './App.css'
import React, { useRef, useState } from 'react';
import axios from "axios";

const Upload = () => {
    // Create a ref for the file input - triggered by the button click
    const fileInputRef = useRef(null);
    // State to hold the selected file
    const [file, setFile] = useState(null);

    // Trigger file picker
    const handleClick = () => {
        fileInputRef.current.click();
    };

    // Capture file
    const handleFileChange = async (e) => {
        const selectedFile = e.target.files[0];
        if (!selectedFile) return;
    
        setFile(selectedFile);

        const formData = new FormData();
        formData.append("image", selectedFile);

        try {
            const res = await axios.post("http://127.0.0.1:5000/recommend", formData)
           
            console.log("Upload success:", res.data);
        } catch (err) {
            console.error("Upload failed:", err);
        }
      };
  return (
    <> 
          <input
              type="file"
              accept="image/*"
              // Use the ref to trigger hidden file input
              ref={fileInputRef}
              style={{ display: "none" }}
              onChange={handleFileChange}
          />
          <div className="uploadButton" onClick={handleClick}>
    
    <div className="uploadText">UPLOAD</div>
    <img
    className="uploadLogo"
    alt="Outline arrows"
    src={upload}
    />
    </div>
      </>
  )
}

export default Upload