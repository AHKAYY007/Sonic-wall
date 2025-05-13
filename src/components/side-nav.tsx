"use client"
import { usePathname } from "next/navigation";
import Link from "next/link";
import Image from "next/image";
function SideNav() {
    const pathName = usePathname();


    const navLinks = [
      { title: "Dashboard", href: "/", icon: "" },
      { title: "Rules", href: "/dashboard/rules", icon: "" },
      { title: "Analytics", href: "/dashboard/analytics", icon: "" },
      { title: "Integration", href: "/dashboard/integration", icon: "" },
      { title: "Settings", href: "/dashboard/settings", icon: "" },
    ];

    return (
        <div className="flex flex-col justify-start items-start p-4 bg-[#061224] w-[20vw]">
        <h1 className="flex justify-start items-center gap-3 font-bold text-2xl">
          <span className="relative h-14 w-14 rounded-2xl overflow-hidden">
            <Image
              alt=" logo"
              src={"/sonic wal logo.jpg"}
              layout="fill"
              objectFit="contain"
              objectPosition="center"
            ></Image>
          </span>
          Sonic Wall
        </h1>
      <nav
        className={`flex flex-col w-full justify-start items-start gap-2 rounded-2xl py-6 px-3`}
      >
        {navLinks.map((link) => (
          <Link
            href={link.href}
            key={link.title}
            className={`text-base opacity-90 py-2 px-4 font-medium w-full rounded-lg ${
              link.href === pathName ? "bg-[#1E2A38] text-[#4DA8DA]" : ""
            }`}
          >
            {link.title}
          </Link>
        ))}
            </nav>
            </div>
    );
}
export default SideNav