import { Camera } from "expo-camera";
import { useEffect, useState } from "react";
import {
  ActivityIndicator,
  Alert,
  ImageBackground,
  SafeAreaView,
  Text,
  TouchableOpacity,
  View,
} from "react-native";
import { colors } from "../components/constants";
import { Ionicons } from "@expo/vector-icons";
import { router } from "expo-router";
import instance from "../axios";
import { BlurView } from "expo-blur";

const HomePage = () => {
  const [hasPermission, setHasPermission] = useState<any>(null);
  const [cameraRef, setCameraRef] = useState<any>(null);
  const [capturedImage, setCapturedImage] = useState<any>(null);
  const [display, setDisplay] = useState<"camera" | "picture">("camera");

  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    (async () => {
      const { status } = await Camera.requestCameraPermissionsAsync();
      setHasPermission(status === "granted");
    })();
  }, []);

  const takePicture = async () => {
    if (cameraRef) {
      const photo = await cameraRef.takePictureAsync();
      setCapturedImage(photo.uri);
      setDisplay("picture");
    }
  };

  const sendOnServer = async () => {
    setIsLoading(true);
    const formData = new FormData();
    formData.append("photo", {
      uri: capturedImage,
      type: "image/jpeg",
      name: "photo.jpg",
    });
    await instance
      .post("/scan_photo", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((res) =>
        router.push({
          pathname: "/info",
          params: {
            audio_path: res.data.audio_path,
            objects: res.data.objects,
            photo_path: res.data.photo_path,
            text: res.data.text,
          },
        })
      )
      .catch((err) => {
        if (err.response.status === 400) {
          Alert.alert(
            "На фото не було розпізнано жодного з туристичних обʼєктів. Будь-ласка, спробуйте ще раз!"
          );
          setIsLoading(false);
        } else {
          Alert.alert("Помилка сервера!");
          setIsLoading(false);
        }
      })
      .finally(() => setIsLoading(false));
    setIsLoading(false);
  };

  if (hasPermission === null) {
    return <View />;
  }
  if (hasPermission === false) {
    return <Text>No access to camera</Text>;
  }

  return (
    <View>
      {display === "camera" ? (
        <Camera
          style={{
            width: "100%",
            height: "100%",
            marginBottom: 25,
            justifyContent: "flex-end",
            alignItems: "center",
          }}
          ref={(ref) => setCameraRef(ref)}
        >
          <SafeAreaView>
            <View
              style={{ borderRadius: 50, overflow: "hidden", marginBottom: 40 }}
            >
              <BlurView intensity={50}>
                <View
                  style={{
                    flexDirection: "row",
                    gap: 15,
                    backgroundColor: "rgba(22, 21, 19, 0.8)",
                    padding: 15,
                    borderRadius: 50,
                  }}
                >
                  <TouchableOpacity
                    onPress={takePicture}
                    style={{
                      backgroundColor: "#161513",
                      borderRadius: 100,
                      borderColor: colors.GREY,
                      borderWidth: 1,
                      padding: 25,
                    }}
                  >
                    <Ionicons name="camera" color="white" size={20} />
                  </TouchableOpacity>
                  <TouchableOpacity
                    onPress={() => setDisplay("picture")}
                    style={{
                      backgroundColor: "#161513",
                      borderRadius: 100,
                      borderColor: capturedImage ? colors.GREY : colors.GREY,
                      borderWidth: 1,
                      padding: 25,
                    }}
                    disabled={capturedImage ? false : true}
                  >
                    <Ionicons
                      name="image"
                      color={capturedImage ? "white" : colors.GREY}
                      size={20}
                    />
                  </TouchableOpacity>
                </View>
              </BlurView>
            </View>
          </SafeAreaView>
        </Camera>
      ) : (
        <ImageBackground
          style={{
            width: "100%",
            height: "100%",
            marginBottom: 25,
            justifyContent: "flex-end",
            alignItems: "center",
          }}
          source={{
            uri: capturedImage,
          }}
        >
          <SafeAreaView>
            <View
              style={{ borderRadius: 50, overflow: "hidden", marginBottom: 40 }}
            >
              <BlurView intensity={50}>
                <View
                  style={{
                    flexDirection: "row",
                    gap: 15,
                    backgroundColor: "rgba(22, 21, 19, 0.8)",
                    padding: 15,
                    borderRadius: 50,
                  }}
                >
                  {!isLoading && (
                    <TouchableOpacity
                      onPress={() => setDisplay("camera")}
                      style={{
                        backgroundColor: "#161513",
                        borderRadius: 100,
                        borderColor: colors.GREY,
                        borderWidth: 1,
                        padding: 25,
                      }}
                    >
                      <Ionicons name="reload" color="white" size={20} />
                    </TouchableOpacity>
                  )}
                  <TouchableOpacity
                    onPress={sendOnServer}
                    style={{
                      backgroundColor: "#161513",
                      borderRadius: 100,
                      borderColor:
                        capturedImage && !isLoading ? colors.GREY : colors.GREY,
                      borderWidth: 1,
                      padding: 25,
                    }}
                    disabled={capturedImage && !isLoading ? false : true}
                  >
                    {!isLoading ? (
                      <Ionicons
                        name="checkmark"
                        color={capturedImage ? "white" : colors.GREY}
                        size={20}
                      />
                    ) : (
                      <ActivityIndicator />
                    )}
                  </TouchableOpacity>
                </View>
              </BlurView>
            </View>
          </SafeAreaView>
        </ImageBackground>
      )}
    </View>
  );
};

export default HomePage;
