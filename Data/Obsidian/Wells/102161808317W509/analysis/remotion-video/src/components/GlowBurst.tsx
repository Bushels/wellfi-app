import React from "react";
import { spring, useCurrentFrame, interpolate } from "remotion";
import { FPS } from "../theme";

interface GlowBurstProps {
  /** Absolute frame when the burst fires */
  triggerFrame: number;
  /** Center X in the parent SVG coordinate space */
  cx: number;
  /** Center Y in the parent SVG coordinate space */
  cy: number;
  /** Burst color (hex) */
  color: string;
  /** Resting radius after the burst settles */
  restRadius?: number;
}

export function GlowBurst({
  triggerFrame,
  cx,
  cy,
  color,
  restRadius = 12,
}: GlowBurstProps): React.ReactElement | null {
  const frame = useCurrentFrame();
  const localFrame = frame - triggerFrame;
  if (localFrame < 0) return null;

  const burst = spring({
    frame: localFrame,
    fps: FPS,
    config: { damping: 12, mass: 0.6, stiffness: 180 },
  });

  // Scale: 0 -> 2.5x rest radius via spring, then settle to 1.2x
  const radius = interpolate(burst, [0, 1], [0, restRadius * 2.5], {
    extrapolateRight: "clamp",
  });

  const finalRadius = localFrame > 24 ? restRadius * 1.2 : radius;

  // Opacity: fade in fast, then settle to 0.25
  const opacity = interpolate(
    localFrame,
    [0, 6, 18, 36],
    [0, 0.4, 0.35, 0.25],
    { extrapolateRight: "clamp" },
  );

  return (
    <circle
      cx={cx}
      cy={cy}
      r={finalRadius}
      fill="none"
      stroke={color}
      strokeWidth={2}
      opacity={opacity}
      style={{
        filter: `drop-shadow(0 0 ${finalRadius * 0.8}px ${color})`,
      }}
    />
  );
}
