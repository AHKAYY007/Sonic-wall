function Heading() {

    return (
      <div className="flex justify-between items-center w-full">
        <h2 className="text-lg font-semibold">Dashboard</h2>
        <button className="p-3 rounded-lg border border-gray-600 hover:opacity-80 cursor-pointer">
          {" "}
          Connect Wallet
        </button>
      </div>
    );
}
export default Heading