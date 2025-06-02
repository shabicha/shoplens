import LensLogo from '/Users/shabichasureshkumar/Desktop/shoplens/frontend/src/assets/shopLogo.svg'
import upload from '/Users/shabichasureshkumar/Desktop/shoplens/frontend/src/assets/upload.svg'
import './App.css'

function App() {
  

  return (
    <>
      
      <img className="logo" alt="Vector" src={LensLogo} />
      <div className="uploadButton">

<div className="uploadText">UPLOAD</div>
<img
className="uploadLogo"
alt="Outline arrows"
src={upload}
/>
</div>

      <div className="Result">Results [100]</div>
      <img 
        className="image" alt="Product Listing" src="https://media-photos.depop.com/b1/11541806/2012181995_2b1bb9fab73c4b25a93d74b00583780a/P8.jpg"
         />
      
    </>
  )
}

export default App
