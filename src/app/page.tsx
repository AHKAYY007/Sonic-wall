import SideNav from "@/components/side-nav";
import Heading from "@/components/heading";

export default function Home() {

 
  return (
    <main className="flex w-full h-full bg-[#1A1F29] relative">
      
       <SideNav />

      <div className="flex flex-col w-full justify-start items-start gap-4 p-4 sm:p-6">
        <Heading />
        <div></div>
      </div>
    </main>
  );
}
