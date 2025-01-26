import nightBed from "../../assets/nightBed.jpg";
import bloodCell from "../../assets/bloodCell.jpg";
import xRay from "../../assets/xray.jpg";

export default function HomePage() {
    return (
        <div>
            <div className="flex flex-col justify-center items-center h-[100vh] bg-custom-purple-gradient">
            <h1 className="text-gray-100 text-6xl font-bold text-center">
                Try NeuroFlow for Free{' '}
                <span className="inset-0 bg-white opacity-20 blur-md transform translate-y-1"></span>
            </h1>
                <h2 className="text-gray-100 text-center pt-4 pb-5 text-4xl max-w-[450px] text-shadow">Convenient HRV data in your pocket</h2>
                <button className="transition ease-in-out hover:bg-slate-950 bg-slate-800 border border-gray-500 text-white rounded-md px-4 py-2">Try NeuroFlow</button>
                {/* <p className="text-gray-100 text-center pt-4 text-shadow">Your journey to better health starts here!</p> */}
            </div>
            <div>
                <div className="h-24 flex justify-center bg-white items-center">
                    <h1 className="text-6xl font-bold mt-16">Here's the facts.</h1>
                </div>
                <div className="h-auto xl:h-[90vh] 2xl:h-[90vh]  flex flex-col xl:flex-row align-center pt-10 xl:pt-0 items-center xl:space-x-12 space-x-0 justify-center bg-white">
                    <div className="xl:w-[25vw] w-[80vw] h-[60vh] xl:h-[650px] flex flex-col items-center justify-center p-4 rounded-2xl border border-black mb-8 shadow-2xl" style={{ backgroundImage: `url(${nightBed})`, backgroundSize: 'cover', backgroundPosition: 'center' }}>
                        <div className="h-[50vh] justify-center">
                            <h1 className="text-left text-white text-3xl px-8 2xl:pt-[270px] lg:pt-[210px] pt-[250px] font-bold">Sleep</h1>
                            <h1 className="text-md xl:text-md text-left px-8 mt-2 text-white">Individuals experiencing high levels of stress have more trouble falling asleep and staying asleep. Prolonged periods of disrupted sleep can result in telomeric shortening, hormonal changes, and a shorter life expectancy.</h1>
                        </div>
                    </div>
                    <div className="xl:w-[25vw] w-[80vw] h-[60vh] xl:h-[650px] flex flex-col items-center justify-center p-4 rounded-2xl border border-black mb-8 shadow-2xl" style={{ backgroundImage: `url(${bloodCell})`, backgroundSize: 'cover', backgroundPosition: 'center' }}>
                        <div className="h-[50vh] justify-center">
                            <h1 className="text-left text-white text-3xl px-8 lg:pt-[210px] 2xl:pt-[270px] pt-[250px] font-bold">Immune System</h1>
                            <h1 className="text-md xl:text-md text-left px-8 mt-2 text-white">Chronic stress can suppress the immune system, making the body more vulnerable to infections and diseases. Prolonged stress negatively affects immune function by reducing the production of white blood cells, leading to increased susceptibility to illness and contributing to premature aging and a reduced lifespan.</h1>
                        </div>
                    </div>
                    <div className="xl:w-[25vw] w-[80vw] h-[60vh] xl:h-[650px] flex flex-col items-center justify-center bg-gray-100 p-4 rounded-2xl border border-black mb-8 shadow-2xl" style={{ backgroundImage: `url(${xRay})`, backgroundSize: 'cover', backgroundPosition: 'center' }}>
                        <div className="h-[50vh] justify-center">
                            <h1 className="text-left text-white text-3xl px-8 2xl:pt-[270px] lg:pt-[210px] pt-[250px] font-bold">Systemic Health</h1>
                            <h1 className="text-md xl:text-md text-left px-8 mt-2 text-white">Chronic stress activates the body's "fight or flight" response, which increases the production of cortisol and adrenaline. Over time, elevated levels of these hormones can lead to increased blood pressure, inflammation, and a higher risk of heart disease and stroke. 
                            </h1>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}