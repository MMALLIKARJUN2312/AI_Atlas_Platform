import {apiClient} from "@/lib/api-client";
import { Problem } from "@/types/problem";

class ProblemService {
  async getProblems(companyId: number | string) {
    const { data } = await apiClient.get<Problem[]>(
      `/companies/${companyId}/problems`
    );

    return data;
  }
}

export const problemService = new ProblemService();