// verse_memorization_screen.dart
import 'package:audioplayers/audioplayers.dart';
import 'package:flutter/material.dart';
import 'package:quran_aider/models/chapter.dart';
import 'package:quran_aider/models/verse.dart';
import 'package:quran_aider/widgets/app_button.dart';

class VerseMemorizationScreen extends StatefulWidget {
  final Chapter chapter;

  const VerseMemorizationScreen({Key? key, required this.chapter})
      : super(key: key);

  @override
  _VerseMemorizationScreenState createState() =>
      _VerseMemorizationScreenState();
}

class _VerseMemorizationScreenState extends State<VerseMemorizationScreen>
    with SingleTickerProviderStateMixin {
  int currentVerseIndex = 0;
  String displayedText = '';
  late AudioPlayer audioPlayer;
  late AnimationController _animationController;
  late Animation<double> _animation;
  bool isLongPressActive = false;
  bool isAudioPlaying = false;

  @override
  void initState() {
    super.initState();
    audioPlayer = AudioPlayer();
    _animationController = AnimationController(
      duration: const Duration(milliseconds: 500),
      vsync: this,
    );
    _animation = Tween<double>(begin: 0, end: 1).animate(_animationController);
  }

  @override
  void dispose() {
    audioPlayer.dispose();
    _animationController.dispose();
    super.dispose();
  }

  void revealWords(String text) async {
    if (!isLongPressActive) return;

    var words = text.split(' ');
    int wordIndex = 0;

    while (wordIndex < words.length && isLongPressActive) {
      setState(() {
        displayedText += (displayedText.isEmpty ? '' : ' ') + words[wordIndex];
        wordIndex++;
      });
      await Future.delayed(const Duration(milliseconds: 100));
    }
  }

  void showTranslation(String translation) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          backgroundColor: Colors.grey[100],
          title: const Text(
            'English Translation:',
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.w500),
          ),
          content: Text(
            translation,
            style: const TextStyle(fontSize: 20, fontStyle: FontStyle.italic),
          ),
          actions: [
            AppButton(onPress: () => Navigator.of(context).pop(), text: "Close")
            // TextButton(
            //   onPressed: () => Navigator.of(context).pop(),
            //   child: const Text('Close'),
            // ),
          ],
        );
      },
    );
  }

  void playAudio(Verse verse) async {
    if (isAudioPlaying) {
      await audioPlayer.stop();
      setState(() {
        isAudioPlaying = false;
      });
    } else {
      final audioPath =
          'data/Abdullah_Basfar_64kbps/${widget.chapter.number.toString().padLeft(3, '0')}${verse.verseNumber.toString().padLeft(3, '0')}.mp3';
      await audioPlayer.play(AssetSource(audioPath));
      setState(() {
        isAudioPlaying = true;
      });
      audioPlayer.onPlayerComplete.listen((event) {
        setState(() {
          isAudioPlaying = false;
        });
      });
    }
  }

  void navigateVerse(int offset) {
    setState(() {
      currentVerseIndex = (currentVerseIndex + offset)
          .clamp(0, widget.chapter.verses.length - 1);
      displayedText = '';
    });
  }

  @override
  Widget build(BuildContext context) {
    final verse = widget.chapter.verses[currentVerseIndex];

    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.black,
        title: Center(
            child: Text(
          widget.chapter.name,
          style: const TextStyle(fontSize: 22, color: Colors.white),
        )),
        leading: IconButton(
          icon: const Icon(
            Icons.arrow_back,
            color: Colors.white,
          ),
          onPressed: () => Navigator.of(context).pop(),
        ),
      ),
      body: GestureDetector(
        onLongPressStart: (_) {
          setState(() {
            isLongPressActive = true;
            displayedText = '';
          });
          revealWords(verse.arabicText);
        },
        onLongPressEnd: (_) {
          setState(() {
            isLongPressActive = false;
          });
        },
        onDoubleTap: () => showTranslation(verse.englishTranslation),
        child: Container(
          color: Colors.black,
          child: Stack(
            children: [
              Center(
                child: AnimatedOpacity(
                  opacity: displayedText.isEmpty ? 0.0 : 1.0,
                  duration: const Duration(milliseconds: 500),
                  child: Text(
                    displayedText,
                    textAlign: TextAlign.center,
                    style: const TextStyle(fontSize: 28, color: Colors.white),
                  ),
                ),
              ),
              Positioned(
                bottom: 20,
                right: 20,
                child: Text(
                  'Verse ${verse.verseNumber}',
                  style: const TextStyle(fontSize: 16, color: Colors.white),
                ),
              ),
              Positioned(
                bottom: 20,
                left: 20,
                child: Row(
                  children: [
                    // ElevatedButton(
                    //   onPressed: currentVerseIndex > 0
                    //       ? () => navigateVerse(-1)
                    //       : null,
                    //   child: const Icon(Icons.arrow_back),
                    // ),
                    AppButton(
                      onPress:
                          currentVerseIndex < widget.chapter.verses.length - 1
                              ? () => navigateVerse(-1)
                              : () {},
                      text: "",
                      icon: Icons.arrow_back,
                    ),
                    const SizedBox(width: 10),
                    // ElevatedButton(
                    //   onPressed:
                    //       currentVerseIndex < widget.chapter.verses.length - 1
                    //           ? () => navigateVerse(1)
                    //           : null,
                    //   child: const Icon(Icons.arrow_forward),
                    // ),
                    AppButton(
                      onPress:
                          currentVerseIndex < widget.chapter.verses.length - 1
                              ? () => navigateVerse(1)
                              : () {},
                      text: "",
                      icon: Icons.arrow_forward,
                    ),
                    const SizedBox(width: 10),
                    AppButton(
                        onPress: () => playAudio(verse),
                        text: isAudioPlaying ? 'Stop Audio' : 'Play Audio'),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
