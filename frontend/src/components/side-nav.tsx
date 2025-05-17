"use client"
import { usePathname } from "next/navigation";
import Link from "next/link";
import Image from "next/image";
function SideNav() {
    const pathName = usePathname();


    const navLinks = [
      {
        title: "Dashboard",
        href: "/",
        icon: "/dashboard.png",
        active: "/dashboard-active.png",
      },
      {
        title: "Rules",
        href: "/dashboard/rules",
        icon: "/rule.png",
        active: "/rule-active.png",
      },
      {
        title: "Analytics",
        href: "/dashboard/analytics",
        icon: "/analytics.png",
        active: "/analytics-active.png",
      },
      {
        title: "Integration",
        href: "/dashboard/integration",
        icon: "/integration.png",
        active: "/integration-active.png",
      },
      {
        title: "Settings",
        href: "/dashboard/settings",
        icon: "/settings.png",
        active: "/settings-active.png",
      },
    ];

    return (
      <>
        {/* // for desktop */}
        <div className="flex flex-col justify-start fixed -left-full transition-class lg:sticky lg:top-0 items-start p-4 bg-[#061224] w-[20vw] min-w-60 max-lg:hidden">
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
                className={`text-base flex opacity-90 py-2 hover:bg-[#1E2A38] transition-class hover:text-[#4DA8DA] px-4 gap-3 font-medium w-full rounded-lg ${
                  link.href === pathName ? "bg-[#1E2A38] text-[#4DA8DA]" : ""
                }`}
              >
                <span className="relative h-6 w-6 flex justify-center items-center">
                  <Image
                    alt={link.title}
                    src={link.active}
                    layout="fill"
                    objectFit="contain"
                    objectPosition="center"
                  ></Image>
                </span>
                {link.title}
              </Link>
            ))}
          </nav>
        </div>
        {/* // for mobile */}
        <div className="flex w-full justify-between shadow-lg fixed bottom-0 left-0 lg:hidden bg-[#1A1F29] h-18 z-[10000] py-1 px-2 gap-1">
          {navLinks.map((link) => (
            <Link
              href={link.href}
              key={link.title}
              className={`text-xs flex flex-col justify-center items-center opacity-90 py-2 px-1 transition-class hover:text-[#4DA8DA] hover:bg-[#4da9da15] sm:px-4 gap-3 font-medium w-full rounded-lg ${
                link.href === pathName
                  ? " text-[#4DA8DA] bg-[#4da9da15]"
                  : "text-[#ffffffa5]"
              }`}
            >
              <span className="relative h-6 w-6 flex justify-center items-center">
                <Image
                  alt={link.title}
                  src={link.active}
                  layout="fill"
                  objectFit="contain"
                  objectPosition="center"
                ></Image>
              </span>
              {link.title}
            </Link>
          ))}
        </div>
      </>
    );
}
export default SideNav