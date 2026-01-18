import upload from '/Users/shabichasureshkumar/Desktop/shoplens/frontend/src/assets/upload.svg'
import './App.css'
import React, { useRef, useState } from 'react';
import axios from "axios";
import x from '/Users/shabichasureshkumar/Desktop/shoplens/frontend/src/assets/x.svg'

const Upload = ({ onResults }) => {  
    // Create a ref for the file input - triggered by the button click
    const fileInputRef = useRef(null);
    // State to hold the selected file
    const [file, setFile] = useState(null);
    //for link pasting
    const [imageUrl, setImageUrl] = useState('');

    // Trigger file picker
    const handleClick = () => {
        fileInputRef.current.click();
    };
    
    const handleReset = () => {
        setFile(null); // 
    };

    // Capture file
    const handleFileChange = async (e) => {
        const selectedFile = e.target.files[0];
        if (!selectedFile) return;
    
        setFile(selectedFile);

        const formData = new FormData();
        formData.append("image", selectedFile);

        try {
            const res = await axios.post("http://127.0.0.1:5000/recommend", formData);
           
            console.log("Upload success:", res.data);
            
            // Send results back to App component
            onResults(res.data);
            
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
    <div className="flex flex-col items-center justify-center gap-6 p-8 w-full">
        <div className="text-black text-sm font-normal text-center">
            drag an image here or{' '}
            <span className="text-blue-500 cursor-pointer">upload a file</span>
        </div>
        
        <div className="flex items-center gap-4 w-full">
            <div className="flex-1 h-[2px] bg-black"></div>
            <span className="text-black text-sm">or</span>
            <div className="flex-1 h-[2px] bg-black"></div>
        </div>
        
     <input
    type="text"
    placeholder="paste image link"
    value={imageUrl}
    onChange={(e) => setImageUrl(e.target.value)}
    onKeyDown={async (e) => {
        if (e.key === 'Enter' && imageUrl.trim()) {
            try {
                // Fetch the image from the URL
                const response = await fetch(imageUrl);
                const blob = await response.blob();
                const file = new File([blob], "pasted-image.jpg", { type: blob.type });
                
                setFile(file);
                
                // Upload to your backend
                const formData = new FormData();
                formData.append("image", file);
                
                const res = await axios.post("http://127.0.0.1:5000/recommend", formData);
                console.log("Upload success:", res.data);
                onResults(res.data);
                
                setImageUrl(''); // Clear the input
            } catch (err) {
                console.error("Failed to load image from URL:", err);
            }
        }
    }}
    className="w-full px-4 py-3 bg-pink-200 border-2 border-black text-black placeholder-black/60 text-sm focus:outline-none"
/>
    </div>
</div>
                )}
            </div>
        </>
    );
};

export default Upload