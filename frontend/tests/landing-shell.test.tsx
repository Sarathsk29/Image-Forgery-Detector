import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { vi } from "vitest";

import { LandingShell } from "@/components/landing-shell";


const push = vi.fn();
const createCase = vi.fn();
const openCase = vi.fn();

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push })
}));

vi.mock("@/lib/api", () => ({
  createCase: (...args: unknown[]) => createCase(...args),
  openCase: (...args: unknown[]) => openCase(...args)
}));


describe("LandingShell", () => {
  it("creates a case and redirects to the case workspace", async () => {
    createCase.mockResolvedValue({
      case_id: "CASE-20260325-ABC123",
      access_key: "AB12-CD34-EF56"
    });

    const user = userEvent.setup();
    render(<LandingShell />);

    await user.type(screen.getByPlaceholderText(/property deed/i), "Tampered deed");
    await user.click(screen.getByRole("button", { name: /create case/i }));

    await waitFor(() => {
      expect(createCase).toHaveBeenCalled();
      expect(push).toHaveBeenCalledWith("/cases/CASE-20260325-ABC123?accessKey=AB12-CD34-EF56");
    });
  });
});

