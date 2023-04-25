import React from "react"
import {
  TimelineItem,
  TimelineSeparator,
  TimelineDot,
  TimelineConnector,
  TimelineContent,
  Timeline,
  timelineItemClasses,
} from "@mui/lab"
import { Box, Typography, styled } from "@mui/material"

const StyledTimelineContent = styled(TimelineContent)(theme => ({
  fontSize: 20,
  color: "#818792",
  paddingTop: theme.theme.spacing(3),
}))

const DotBox = styled(Box)(theme => ({
  width: 40,
  height: 40,
  fontSize: 24,
  fontWeight: "bold",
  textAlign: "center",
  paddingTop: theme.theme.spacing(0.25),
}))

const StyledTimelineDot = styled(TimelineDot)(() => ({
  borderColor: "#8338EC",
  color: "#8338EC",
  textAlign: "center",
}))

const ValueProp: React.FC = () => (
  <Box sx={{ mt: 5 }}>
    <Typography variant="h6" sx={{ fontSize: 22 }}>
      Get started for free
    </Typography>
    <Timeline
      sx={{
        pl: 0,
        [`& .${timelineItemClasses.root}:before`]: {
          flex: 0,
          padding: 0,
        },
      }}
    >
      <TimelineItem>
        <TimelineSeparator>
          <StyledTimelineDot variant="outlined">
            <DotBox>1</DotBox>
          </StyledTimelineDot>
          <TimelineConnector sx={{ height: 15 }} />
        </TimelineSeparator>
        <StyledTimelineContent>Connect your data sources</StyledTimelineContent>
      </TimelineItem>
      <TimelineItem>
        <TimelineSeparator>
          <StyledTimelineDot variant="outlined">
            <DotBox>2</DotBox>
          </StyledTimelineDot>
          <TimelineConnector sx={{ height: 15 }} />
        </TimelineSeparator>
        <StyledTimelineContent>Integrate with GitHub</StyledTimelineContent>
      </TimelineItem>
      <TimelineItem>
        <TimelineSeparator>
          <StyledTimelineDot variant="outlined">
            <DotBox>3</DotBox>
          </StyledTimelineDot>
        </TimelineSeparator>
        <StyledTimelineContent>
          Open a pull request and run tests
        </StyledTimelineContent>
      </TimelineItem>
    </Timeline>
  </Box>
)

export default ValueProp
