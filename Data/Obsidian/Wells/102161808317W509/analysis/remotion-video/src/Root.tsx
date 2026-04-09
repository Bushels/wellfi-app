import { Composition } from "remotion";
import { DeploymentStory } from "./DeploymentStory";
import { DeploymentStoryV2 } from "./DeploymentStoryV2";
import { Run3Storyboard } from "./run3/Run3Storyboard";
import { Run3StoryboardShort } from "./run3/Run3StoryboardShort";
import { WIDTH, HEIGHT, FPS, DURATION_FRAMES } from "./theme";
import { RUN3_DURATION_FRAMES, RUN3_SHORT_DURATION_FRAMES } from "./run3/run3Data";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="DeploymentStory"
        component={DeploymentStory}
        durationInFrames={DURATION_FRAMES}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />
      <Composition
        id="DeploymentStoryV2"
        component={DeploymentStoryV2}
        durationInFrames={1080}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />
      <Composition
        id="DeploymentStoryRun3"
        component={Run3Storyboard}
        durationInFrames={RUN3_DURATION_FRAMES}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />
      <Composition
        id="DeploymentStoryRun3Short"
        component={Run3StoryboardShort}
        durationInFrames={RUN3_SHORT_DURATION_FRAMES}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />
    </>
  );
};
