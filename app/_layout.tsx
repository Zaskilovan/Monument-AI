import { Stack } from "expo-router";

const RootLayout = () => {
  return (
    <Stack
      screenOptions={{
        headerShown: false,
        contentStyle: {
          backgroundColor: "#DCE1E3",
        },
      }}
    >
      <Stack.Screen name="index" />
      <Stack.Screen name="home" />
    </Stack>
  );
};

export default RootLayout;
