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
      
      <div class ="h-[50px] w-[158px]">
<p className="text-black text-[13.2px] font-normal tracking-[0] leading-[normal] fixed w-[158px] left-0 top-0 [font-family:'JetBrain-Reg']">
Comme des Garçons Men&#39;s White and Red Trainers
</p>
</div>
      
    </>
  )
}

export default App
