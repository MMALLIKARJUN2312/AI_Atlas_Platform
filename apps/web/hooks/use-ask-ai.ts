import { useMutation } from "@tanstack/react-query";

import { aiService } from "@/services";

export function useAskAI() {
  return useMutation({
    mutationFn: (question: string) => aiService.ask(question),
  });
}
