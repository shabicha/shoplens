import LensLogo from '/Users/shabichasureshkumar/Desktop/shoplens/frontend/src/assets/shopLogo.svg'
import './App.css'
import Upload from './Upload'
import arrow from '/Users/shabichasureshkumar/Desktop/shoplens/frontend/src/assets/arrow.svg'

function App() {
  

  return (
    <>
      
      <img className="logo" alt="Vector" src={LensLogo} />
      <Upload/>

      <div className="Result">Results [100]</div>

<div className="flex flex-col gap-2 w-[228px] h-[228px] items-start ml-16">
  <img
    className="w-full object-cover block"
    alt="Product Listing"
    src="https://media-photos.depop.com/b1/11541806/2012181995_2b1bb9fab73c4b25a93d74b00583780a/P8.jpg"
  />
<div className ="flex flex-row gap-10">
  <div className='gap-11'> 
  <p className="text-black text-[13.2px] font-normal w-[160px] leading-normal font-['JetBrain-Reg']">
    Comme des Garçons Men's White and Red Trainers
  </p>
  <div className=" text-black text-[22px] font-bold w-[158px] left-0 top-[60px] font-['JetBrain-Bold']">$78.00</div>
</div>

<div className="items-center bg-[#8ae574] flex gap-[11px] h-[82.5px] justify-center relative w-[35.2px] px-[16.5px] py-[25.3px] rounded-[2px] border-[2.2px] border-solid border-black">
  <div className="h-[16px] ml-[-5.50px] mr-[-5.50px] relative w-[13.2px]"> 
<img className="vector" alt="Vector" src={arrow} />
</div>
</div>
</div>
</div>

      
    </>
  )
}

export default App
