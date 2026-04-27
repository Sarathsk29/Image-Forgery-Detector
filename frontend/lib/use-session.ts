import { useEffect, useState } from "react";
import { createCase } from "@/lib/api";

export type ForensiqSession = {
  caseId: string;
  accessKey: string;
};

export function useSession() {
  const [session, setSession] = useState<ForensiqSession | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    const initializeSession = async () => {
      const stored = window.localStorage.getItem("forensiq_session");
      if (stored) {
        try {
          const parsed = JSON.parse(stored);
          if (parsed.caseId && parsed.accessKey) {
            if (!cancelled) setSession(parsed);
            return;
          }
        } catch {
          // Bad format
        }
      }
      try {
        const res = await createCase({ title: "Analysis Session", notes: "Auto-generated analysis workspace." });
        const newSession = { caseId: res.case_id, accessKey: res.access_key };
        window.localStorage.setItem("forensiq_session", JSON.stringify(newSession));
        if (!cancelled) setSession(newSession);
      } catch (err) {
        if (!cancelled) setError("Failed to initialize system session.");
      }
    };

    void initializeSession();

    return () => {
      cancelled = true;
    };
  }, []);

  return { session, error };
}
