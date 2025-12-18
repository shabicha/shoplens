import LensLogo from '/Users/shabichasureshkumar/Desktop/shoplens/frontend/src/assets/shopLogo.svg'
import './App.css'
import Upload from './Upload'
import arrow from '/Users/shabichasureshkumar/Desktop/shoplens/frontend/src/assets/arrow.svg'

function App() {
  

  return (
    <>

      

      <div className ="flex flex-col gap-16">

      <Upload/>

<div className="bg-white flex flex-col gap-[26.4px] px-[18.7px] py-[16.5px] rounded-[4.4px] border-[2.2px] border-black w-[280px] ml-16">
    {/* ⬆️ ml-16 */}

<div className="flex flex-col gap-7 w-full items-start">
  <img
    className="w-full object-cover rounded-[6px] border-[2.2px] border-solid border-black block"
    alt="Product Listing"
    src="https://media-photos.depop.com/b1/11541806/2012181995_2b1bb9fab73c4b25a93d74b00583780a/P8.jpg"
  />
<div className ="flex flex-row gap-10">
  <div className='flex flex-col gap-3'> 
  <p className="text-black text-[13.2px] font-normal w-[160px] leading-normal font-['JetBrain-Reg']">
    Comme des Garçons Men's White and Red Trainers
  </p>
  <div className=" text-black text-[22px] font-bold w-[158px] left-0 top-[60px] font-['JetBrain-Bold']">$78.00</div>
</div>

<div className="items-center bg-[#8ae574] flex gap-[11px] h-[95px] justify-center relative w-[35.2px] px-[16.5px] py-[25.3px] rounded-[2px] border-[2.2px] border-solid border-black">
  <div className="h-[16px] ml-[-5.50px] mr-[-5.50px] relative w-[13.2px]"> 
    <div className="h-[54px] w-[54px] relative">

<img alt="Vector" src={arrow} />
</div>
</div>
</div>
</div>
</div>
</div>
      </div>

      
    </>
  )
}

export default App
