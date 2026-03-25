import React from "react";
import { render, screen } from "@testing-library/react";

import { StatusBadge } from "@/components/status-badge";


describe("StatusBadge", () => {
  it("renders readable status labels", () => {
    render(<StatusBadge value="processing" />);
    expect(screen.getByText("processing")).toBeInTheDocument();
  });
});

