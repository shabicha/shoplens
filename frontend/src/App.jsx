import LensLogo from '/Users/shabichasureshkumar/Desktop/shoplens/frontend/src/assets/shopLogo.svg'
import './App.css'
import Upload from './Upload'
function App() {
  

  return (
    <>
      
      <img className="logo" alt="Vector" src={LensLogo} />
      <Upload/>

      <div className="Result">Results [100]</div>
      <img 
        className="image" alt="Product Listing" src="https://media-photos.depop.com/b1/11541806/2012181995_2b1bb9fab73c4b25a93d74b00583780a/P8.jpg"
         />
      
    </>
  )
}

export default App
