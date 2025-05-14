import Image from "next/image";
function Heading() {

    return (
      <div className="flex justify-between items-center w-full">
        <div className="flex justify-start items-center gap-3">
          <h1 className="flex justify-start items-center gap-3 font-bold text-2xl lg:hidden">
            <span className="relative h-12 w-12 md:h-14 md:w-14 rounded-2xl overflow-hidden">
              <Image
                alt=" logo"
                src={"/sonic wal logo.jpg"}
                layout="fill"
                objectFit="contain"
                objectPosition="center"
              ></Image>
            </span>
            <span className="max-sm:hidden">Sonic Wall</span>
          </h1>
          <h2 className="text-lg font-semibold max-lg:hidden">Dashboard</h2>
        </div>
        <button className="p-3 rounded-lg border border-gray-600 hover:opacity-80 cursor-pointer">
          {" "}
          Connect Wallet
        </button>
      </div>
    );
}
export default Heading