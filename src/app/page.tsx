import SideNav from "@/components/side-nav";
import Heading from "@/components/heading";
import FlexCard from "@/components/flex-card";
import TrafficCard from "@/components/traffic-card";
import PageTransitionEffect from "@/components/page-transition-effect";
import GetStarted from "@/components/get-started-card";
import IntegrationCard from "@/components/integration-card";
import BlockedCard from "@/components/blocked-card";
export default function Home() {
  const data = [
    { title: "Total Calls", value: "12,840", unit: "" },
    { title: "% Blocked", value: "7.1", unit: " % " },
    { title: "Average Latency", value: "204", unit: "ms" },
  ];
 
  return (
    <PageTransitionEffect>
      <main className="flex w-full h-full bg-[#1A1F29] relative max-lg:pb-18">
        <SideNav />

        <div className="flex flex-col w-full justify-start items-start gap-4 pt-4 pl-4 pr-4 pb-8 sm:pt-6 sm:pl-6 sm:pr-6 sm:pb-10 overflow-y-scroll">
          <Heading />
          <div className="flex gap-3 justify-start items-center w-full flex-wrap lg:flex-nowrap">
            {data.map((data, index) => (
              <FlexCard
                title={data.title}
                unit={data.unit}
                value={data.value}
                key={index}
              />
            ))}
          </div>
          <div className="flex gap-4 w-full lg:flex-nowrap flex-wrap  justify-between items-start">
            <div className="flex w-full lg:w-[60%] flex-col justify-start items-start gap-4">
              <TrafficCard />
              {/* integration wizard */}
              <IntegrationCard />
            </div>
            <div className="flex w-full lg:w-[40%] flex-col justify-start items-start gap-4 max-lg:mb-18">
              <BlockedCard />
              <GetStarted />
            </div>
          </div>
        </div>
      </main>
    </PageTransitionEffect>
  );
}
