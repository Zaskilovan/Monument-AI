import { Ionicons } from "@expo/vector-icons";
import { useLocalSearchParams } from "expo-router";
import { useEffect, useState } from "react";
import {
  ActivityIndicator,
  Animated,
  Image,
  SafeAreaView,
  ScrollView,
  Text,
  TouchableOpacity,
  View,
} from "react-native";
import { Audio } from "expo-av";
import { colors } from "../components/constants";

const Info = () => {
  const params = useLocalSearchParams();

  const { audio_path, photo_path, text } = params;

  const [picture, setPicture] = useState<any>();
  const [isLoadingPicture, setIsLoadingPicture] = useState(false);

  const [audio, setAudio] = useState<any>();
  const [soundd, setSoundd] = useState<any>();
  const [play, setPlay] = useState<any>(false);

  const [animatedText, setAnimatedText] = useState("");
  const [opacity] = useState(new Animated.Value(0));

  const fetchMedia = async () => {
    setIsLoadingPicture(true);
    await fetch("http://127.0.0.1:8000/get_media", {
      method: "POST",
      body: JSON.stringify({
        path: photo_path,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.blob())
      .then((blob) => {
        const reader = new FileReader();
        reader.onloadend = () => {
          setPicture(reader.result);
        };
        reader.readAsDataURL(blob);
      });
    setIsLoadingPicture(false);
  };

  const fetchAudio = async () => {
    await fetch("http://127.0.0.1:8000/get_media", {
      method: "POST",
      body: JSON.stringify({
        path: audio_path,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.blob())
      .then((blob) => {
        const reader = new FileReader();
        reader.onloadend = () => {
          setAudio(reader.result);
          handleAudio();
        };
        reader.readAsDataURL(blob);
      });
  };

  const handleAudio = async () => {
    setPlay(!play);

    if (!soundd) {
      const { sound } = await Audio.Sound.createAsync({
        uri: audio,
      });

      if (play) {
        await sound.playAsync();
      } else {
        await sound.stopAsync();
      }

      setSoundd(sound);
    } else {
      if (play) {
        await soundd.playAsync();
      } else {
        await soundd.stopAsync();
      }
    }
  };

  useEffect(() => {
    fetchMedia();
    fetchAudio();
  }, []);

  useEffect(() => {
    const animateTyping = () => {
      const typingSpeed = 25;
      const textToType: any = text;

      let index = 0;
      const typingInterval = setInterval(() => {
        if (index === textToType.length) {
          clearInterval(typingInterval);
        } else {
          setAnimatedText(textToType.slice(0, index + 1));
          index++;
        }
      }, typingSpeed);
    };

    Animated.timing(opacity, {
      toValue: 1,
      duration: 1000,
      useNativeDriver: true,
    }).start();

    animateTyping();

    return () => {};
  }, [opacity]);

  return (
    <SafeAreaView>
      <View style={{ paddingHorizontal: 20 }}>
        {!isLoadingPicture ? (
          <Image
            source={{
              uri: picture,
            }}
            style={{
              width: "100%",
              height: 250,
              borderRadius: 30,
              marginBottom: 20,
            }}
          />
        ) : (
          <View
            style={{
              width: "100%",
              height: 250,
              borderRadius: 30,
              marginBottom: 20,
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <ActivityIndicator />
          </View>
        )}
        <TouchableOpacity
          style={{
            flexDirection: "row",
            alignItems: "center",
            gap: 6,
            marginBottom: 20,
          }}
          onPress={handleAudio}
        >
          {play ? (
            <Ionicons name="volume-high" color={colors.MAIN} />
          ) : (
            <Ionicons name="pause" color={colors.MAIN} />
          )}
          <Text style={{ color: colors.MAIN }}>Аудіо</Text>
        </TouchableOpacity>
        <ScrollView
          style={{
            height: "50%",
          }}
        >
          <Animated.Text
            style={{
              fontFamily: "Montserrat_400Regular",
              color: "black",
            }}
          >
            {animatedText}
          </Animated.Text>
        </ScrollView>
        <TouchableOpacity
          style={{
            flexDirection: "row",
            borderColor: colors.MAIN,
            borderWidth: 1,
            justifyContent: "center",
            alignItems: "center",
            padding: 15,
            borderRadius: 30,
            marginTop: 20,
            gap: 6,
          }}
        >
          <Ionicons name="cash" size={16} color={colors.MAIN} />
          <Text style={{ fontWeight: "600", color: colors.MAIN }}>
            Задонатити
          </Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
};

export default Info;
