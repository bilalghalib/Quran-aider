// chapter.dart
import 'package:quran_memorization_app/models/verse.dart';

class Chapter {
  final int number;
  final String name;
  final List<Verse> verses;

  Chapter({required this.number, required this.name, required this.verses});
}
