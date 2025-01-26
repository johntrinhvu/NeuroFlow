import nightBed from "../../assets/nightBed.jpg";

export default function HomePage() {
    return (
        <div>
            <div className="flex flex-col justify-center items-center h-[100vh] bg-custom-purple-gradient">
            <h1 className="text-gray-100 text-6xl font-bold text-center relative">
                Try NeuroFlow for free{' '}
                <span className="absolute inset-0 bg-white opacity-20 blur-md transform translate-y-1"></span>
            </h1>
                <h2 className="text-gray-100 text-center pt-4 pb-5 text-4xl max-w-[450px] text-shadow">Convenient HRV data in your pocket</h2>
                <button className="bg-black border border-gray-500 w-[100px] text-white rounded-md px-4 py-2">Try It!</button>
                {/* <p className="text-gray-100 text-center pt-4 text-shadow">Your journey to better health starts here!</p> */}
            </div>
            <div className="h-[120vh] flex flex-col align-center justify-center bg-gray-100">
                <div className="h-[33.33vh] flex items-center mx-60 justify-center bg-gray-100 p-4 rounded-lg border border-black mb-8 shadow-lg">
                    <div className="w-[50vw] flex justify-center">
                        <h1 className="text-xl text-center px-8 py-12 text-gray-800">One of the most prevalent symptoms of chronic stress is disrupted sleep, which can manifest as difficulty falling asleep, staying asleep, or experiencing restless, non-refreshing sleep. Stress often keeps the mind racing with worries and concerns, preventing the body from entering a restful state. Over time, this lack of quality sleep can lead to insomnia, further exacerbating stress and leading to a vicious cycle of exhaustion and anxiety.</h1>
                    </div>
                    <div className="w-[50vw] items-center flex justify-center">
                        {/* <div className="flex items-center justify-center w-24 h-24 rounded-full  bg-black text-white text-4xl font-bold">1</div> */}
                        <img src={nightBed} alt="Night Bed" className="w-[500px] h-[300px] rounded-lg" />
                    </div>
                </div>
                <div className="h-[33.33vh] flex items-center mx-60 justify-center bg-gray-100 p-4 rounded-lg border border-black mb-8 shadow-lg">
                    <div className="w-[50vw] flex items-center justify-center">
                        <div className="flex items-center justify-center w-24 h-24 rounded-full bg-black text-white text-4xl font-bold">2</div>
                    </div>
                    <div className="w-[50vw] flex justify-center">
                        <h1 className="text-xl text-center px-8 py-12 text-gray-800">One of the cognitive symptoms of chronic stress is a reduced ability to focus and concentrate. When stress overwhelms the mind, it becomes increasingly difficult to focus on tasks, make decisions, or process information effectively. This mental fog can lead to decreased productivity at work or school, and may also affect daily tasks, such as remembering appointments or following through on responsibilities.</h1>
                    </div>
                </div>
                <div className="h-[33.33vh] flex items-center mx-60 justify-center bg-gray-100 p-4 rounded-lg border border-black mb-8 shadow-lg">
                    <div className="w-[50vw] flex justify-center">
                        <h1 className="text-xl text-center px-8 py-12 text-gray-800">Chronic stress significantly impacts emotional well-being, often leading to emotional instability. Individuals under prolonged stress may experience mood swings, irritability, or sudden outbursts of anger. They may also feel overwhelmed by sadness, helplessness, or a sense of hopelessness. These emotional responses are often disproportionate to the immediate situation, as the accumulated effects of stress heighten sensitivity to daily challenges.</h1>
                    </div>
                    <div className="w-[50vw] flex items-center justify-center">
                        <div className="flex items-center justify-center w-24 h-24 rounded-full bg-black text-white text-4xl font-bold">3</div>
                    </div>
                </div>
            </div>
        </div>
    );
}