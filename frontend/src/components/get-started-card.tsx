import Image from "next/image";

export default function GetStarted() {
    return (
      <div className="flex border border-gray-700 rounded-lg p-4 cursor-pointer hover:bg-[#2789be0f] w-full h-full justify-center items-center flex-col gap-4 transition-class">
        <span className="flex justify-center items-center bg-[#2789be1f] rounded-full p-3">
          <span className="relative flex justify-center items-center h-20 w-20 rounded-full overflow-hidden">
            <Image
              alt="icon"
              src="/fa-solid--plug.png"
              layout="fill"
              objectFit="contain"
              objectPosition="center"
            ></Image>
          </span>
        </span>
        <h2 className="text-lg font-medium opacity-90">
          Get started with Sonic Wall
        </h2>
      </div>
    );
}