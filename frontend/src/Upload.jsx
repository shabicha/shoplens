import upload from '/Users/shabichasureshkumar/Desktop/shoplens/frontend/src/assets/upload.svg'
import './App.css'
import React, { useRef, useState } from 'react';
import axios from "axios";
import x from '/Users/shabichasureshkumar/Desktop/shoplens/frontend/src/assets/x.svg'
const Upload = () => {
    // Create a ref for the file input - triggered by the button click
    const fileInputRef = useRef(null);
    // State to hold the selected file
    const [file, setFile] = useState(null);

    // Trigger file picker
    const handleClick = () => {
        fileInputRef.current.click();
    };
     const handleReset = () => {
    setFile(null); // 👈 reset to default state
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
          <div
        className="uploadButton "
        onClick={handleClick}
      >

    {file ? (
        <div className="flex flex-row gap-48 items-center ">
          <img
            src={URL.createObjectURL(file)}
            alt="Uploaded"
            className="w-12 h-12 rounded-[2px] object-cover outline-solid outline-[2px] outline-black"
          />

 <div onClick={handleReset}
 className="flex flex-col justify-center items-center w-[100px] h-[64px] bg-[#C837AB] border-l-[2px] border-black">
<img
className="w-6 h-6"
src={x}
/>
</div>

</div>

          
        ) : (
          /* Default state */
          <div className="flex flex-col items-center">
            <span className="text-black text-[13.2px] font-normal w-[160px] leading-normal font-['JetBrain-Reg'] pl-12">UPLOAD</span>
          </div>
        )}
      </div>
    </>
  );
};

export default Upload