import { Stack } from "expo-router";

const RootLayout = () => {
  return (
    <Stack
      screenOptions={{
        headerShown: false,
        contentStyle: {
          backgroundColor: "#0E0E0E",
        },
      }}
    >
      <Stack.Screen name="index" />
      <Stack.Screen name="home" />
    </Stack>
  );
};

export default RootLayout;
