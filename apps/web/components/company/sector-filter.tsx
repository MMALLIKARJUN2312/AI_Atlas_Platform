"use client";

import { Sector } from "@/types/sector";
import { Layers3 } from "lucide-react";

interface SectorFilterProps {
  sectors: Sector[];
  selectedSector: string;
  onSelect: (sector: string) => void;
}

export function SectorFilter({
  sectors,
  selectedSector,
  onSelect,
}: SectorFilterProps) {
  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <Layers3
          size={18}
          className="text-blue-500"
        />

        <h2 className="text-lg font-semibold text-white">
          Filter by Sector
        </h2>
      </div>

      <div className="flex flex-wrap gap-2">
        <button
          onClick={() => onSelect("")}
          className={`rounded-lg border px-4 py-2 text-sm font-medium transition ${
            selectedSector === ""
              ? "border-blue-500 bg-blue-600 text-white"
              : "border-zinc-800 bg-zinc-900 text-zinc-400 hover:border-zinc-700 hover:text-white"
          }`}
        >
          All
        </button>

        {sectors.map((sector) => {
          const active =
            selectedSector === sector.segment_name;

          return (
            <button
              key={sector.id}
              onClick={() =>
                onSelect(sector.segment_name)
              }
              className={`rounded-lg border px-4 py-2 text-sm font-medium transition ${
                active
                  ? "border-blue-500 bg-blue-600 text-white"
                  : "border-zinc-800 bg-zinc-900 text-zinc-400 hover:border-zinc-700 hover:text-white"
              }`}
            >
              {sector.segment_name}
            </button>
          );
        })}
      </div>
    </div>
  );
}
