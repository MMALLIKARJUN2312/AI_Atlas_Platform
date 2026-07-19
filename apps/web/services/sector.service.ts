import {apiClient} from "@/lib/api-client";
import { Sector } from "@/types/sector";

class SectorService {
  async getSectors() {
    const { data } = await apiClient.get<Sector[]>(
      "/sectors"
    );

    return data;
  }
}

export const sectorService = new SectorService();