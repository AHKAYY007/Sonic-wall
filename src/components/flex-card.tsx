
type FlexCardProps = {
  title: string;
  value: string;
};

export default function FlexCard({ title, value }: FlexCardProps) {
  return (
    <div
      //   key={key}
      className="flex px-4 py-3 w-full gap-4 flex-col justify-center items-start bg-[#2C3440] rounded-xl"
    >
      <span className="text-base font-normal opacity-85">{title}</span>
      <span className="font-bold text-3xl">{value}</span>
    </div>
  );
}
