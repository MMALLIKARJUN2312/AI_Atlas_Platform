"use client";

import { X } from "lucide-react";
import { AnimatePresence, motion } from "framer-motion";

import { IconButton } from "@/components/ui";
import { Sidebar } from "./sidebar";

interface MobileSidebarProps {
  open: boolean;
  onClose: () => void;
}

export function MobileSidebar({
  open,
  onClose,
}: MobileSidebarProps) {
  return (
    <AnimatePresence>
      {open && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 z-40 bg-black/60 backdrop-blur-sm lg:hidden"
          />

          <motion.div
            initial={{ x: -320 }}
            animate={{ x: 0 }}
            exit={{ x: -320 }}
            transition={{
              type: "spring",
              stiffness: 280,
              damping: 28,
            }}
            className="fixed left-0 top-0 z-50 h-screen w-80 p-4 lg:hidden"
          >
            <div className="absolute right-8 top-8">
              <IconButton
                onClick={onClose}
                aria-label="Close navigation"
              >
                <X size={18} />
              </IconButton>
            </div>

            <Sidebar />
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}