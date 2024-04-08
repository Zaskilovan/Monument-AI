import { Image, Text, TouchableOpacity, View } from "react-native";
import {
  PlayfairDisplaySC_400Regular,
  useFonts,
} from "@expo-google-fonts/playfair-display-sc";
import { Montserrat_300Light } from "@expo-google-fonts/montserrat";
import { colors } from "../components/constants";
import { Ionicons } from "@expo/vector-icons";
import { router } from "expo-router";

const WelcomePage = () => {
  let [fontsLoaded, fontError] = useFonts({
    PlayfairDisplaySC_400Regular,
    Montserrat_300Light,
  });

  if (!fontsLoaded && !fontError) {
    return null;
  }

  return (
    <View
      style={{
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
        marginHorizontal: 20,
      }}
    >
      <Image source={require("../assets/UI/welcome.png")} />
      <Text
        style={{
          fontFamily: "PlayfairDisplaySC_400Regular",
          fontSize: 40,
          color: colors.MAIN,
          marginBottom: 20,
        }}
      >
        Monument AI
      </Text>
      <Text
        style={{
          width: 264,
          fontFamily: "Montserrat_300Light",
          fontSize: 12,
          color: colors.GREY,
          textAlign: "center",
        }}
      >
        MONAI - is a powerful ai tool that provides an information about
        monuments in Ukraine.
      </Text>
      <View
        style={{
          backgroundColor: colors.GREY,
          height: 1,
          width: "50%",
          marginTop: 30,
          marginBottom: 30,
        }}
      ></View>
      <TouchableOpacity
        style={{
          backgroundColor: "#161513",
          borderRadius: 100,
          borderColor: colors.MAIN,
          borderWidth: 1,
          padding: 30,
        }}
        onPress={() => router.replace("/home")}
      >
        <Ionicons name="chevron-forward" color={"white"} size={20} />
      </TouchableOpacity>
    </View>
  );
};

export default WelcomePage;
