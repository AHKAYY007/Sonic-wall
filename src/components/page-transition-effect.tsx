"use client"
import { motion } from "framer-motion";

export default function PageTransitionEffect({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
    return (
        <motion.div
            className="flex w-full h-full"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{duration:.4}}
        >{children}
        </motion.div>
    )
}
