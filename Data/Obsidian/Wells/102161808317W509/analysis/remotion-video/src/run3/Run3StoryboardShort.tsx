import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { COLORS, FONTS } from "../theme";

function rgba(hex: string, alpha: number): string {
  const clean = hex.replace("#", "");
  const normalized =
    clean.length === 3
      ? clean.split("").map((c) => `${c}${c}`).join("")
      : clean;
  const r = Number.parseInt(normalized.slice(0, 2), 16);
  const g = Number.parseInt(normalized.slice(2, 4), 16);
  const b = Number.parseInt(normalized.slice(4, 6), 16);
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

export const Run3StoryboardShort: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(circle at 18% 10%, ${rgba(COLORS.bgGrad, 0.95)} 0%, ${COLORS.bg} 58%)`,
        fontFamily: FONTS.body,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <div style={{ textAlign: "center" }}>
        <div
          style={{
            color: COLORS.cyan,
            fontFamily: FONTS.title,
            fontSize: 64,
            fontWeight: 500,
            letterSpacing: "-0.04em",
            textShadow: `0 0 24px ${rgba(COLORS.cyan, 0.45)}`,
          }}
        >
          WellFi Run 3
        </div>
        <div
          style={{
            color: rgba(COLORS.text, 0.6),
            fontFamily: FONTS.body,
            fontSize: 28,
            marginTop: 16,
          }}
        >
          30-second trimmed cut — placeholder (frame {frame})
        </div>
      </div>
    </AbsoluteFill>
  );
};
