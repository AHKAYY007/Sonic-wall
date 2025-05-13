import SideNav from "@/components/side-nav";
import Heading from "@/components/heading";
import FlexCard from "@/components/flex-card";
import TrafficCard from "@/components/traffic-card";
export default function Home() {
  const data = [
  {title:"Total Calls", value:"12,840"},
  {title:"% Blocked", value:"7.1%"},
  {title:"Average Latency", value:"204 ms"},
]
 
  return (
    <main className="flex w-full h-full bg-[#1A1F29] relative overflow-y-scroll">
      
       <SideNav />

      <div className="flex flex-col w-full justify-start items-start gap-4 p-4 sm:p-6">
        <Heading />
        <div className="flex gap-3 justify-start items-center w-full flex-wrap lg:flex-nowrap">
          {data.map((data, index) => (
            <FlexCard title={data.title} value={data.value} key={index}/>
          ))}
        </div>
        <div className="flex w-full justify-start items-start gap-4">
          <TrafficCard />
        </div>
      </div>
    </main>
  );
}
