import React from "react";
import { Easing, interpolate, useCurrentFrame } from "remotion";

interface NumberCounterProps {
  /** The target number to count to */
  target: number;
  /** Absolute frame when counting starts */
  startFrame: number;
  /** How many frames the count takes (default 18) */
  duration?: number;
  /** Number to start counting from (default 0) */
  from?: number;
  /** Prefix string (e.g. "-" for negative display) */
  prefix?: string;
  /** Suffix string (e.g. " kPa", " dBV", "%", " min") */
  suffix?: string;
  /** Decimal places (default 0) */
  decimals?: number;
  /** CSS style for the container span */
  style?: React.CSSProperties;
}

export function NumberCounter({
  target,
  startFrame,
  duration = 18,
  from = 0,
  prefix = "",
  suffix = "",
  decimals = 0,
  style,
}: NumberCounterProps): React.ReactElement {
  const frame = useCurrentFrame();

  const value = interpolate(
    frame,
    [startFrame, startFrame + duration],
    [from, target],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );

  // Fade in when counting begins — don't show "0" before the counter starts
  const opacity = interpolate(
    frame,
    [startFrame - 6, startFrame + 4],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.quad) },
  );

  const display = `${prefix}${value.toFixed(decimals)}${suffix}`;

  return (
    <span
      style={{
        fontVariantNumeric: "tabular-nums",
        opacity,
        ...style,
      }}
    >
      {display}
    </span>
  );
}
