
export default function TrafficCard() {
    const tableHeaders = ["Timestamp", "Sender", "Address", "Method"];
    const transactions = [
        {time:"2:45 PM", sender:"0x9b1..d02a", address:"0x5fc...ef91", method:"transfer"},
        {time:"2:45 PM", sender:"0x9b1..d02a", address:"0x5fc...ef91", method:"withdraw"},
        {time:"2:45 PM", sender:"0x9b1..d02a", address:"0x5fc...ef91", method:"transfer"},
        {time:"2:45 PM", sender:"0x9b1..d02a", address:"0x5fc...ef91", method:"transfer"},
    ]
    return (
      <div className="w-full bg-[#161a23] text-white border border-gray-700 rounded-lg p-4">
        <h2 className="text-lg font-semibold mb-4 text-left">
          Contract Traffic
        </h2>
        <div className="overflow-x-auto">
          <table className="w-full border-collapse">
            <thead className="text-base opacity-80 font-normal">
              <tr>
                {tableHeaders.map((header, index) => (
                  <th key={index} className="text-left py-2 px-4">
                    {header}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="">
              {transactions.map((transaction, index) => (
                <tr key={index} className="hover:bg-[#232932] odd:bg-[#2c3440b5] cursor-default opacity-90">
                  <td className="py-2 px-4">{transaction.time}</td>
                  <td className="py-2 px-4">{transaction.sender}</td>
                  <td className="py-2 px-4">{transaction.address}</td>
                  <td className="py-2 px-4">{transaction.method}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
}