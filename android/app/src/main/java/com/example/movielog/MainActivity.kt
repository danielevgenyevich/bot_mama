package com.example.movielog

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel

class MainActivity : ComponentActivity() {
	override fun onCreate(savedInstanceState: Bundle?) {
		super.onCreate(savedInstanceState)
		setContent {
			MaterialTheme {
				MovieLogApp()
			}
		}
	}
}

@Composable
fun MovieLogApp(viewModel: MovieViewModel = viewModel()) {
	val movies by viewModel.movies.collectAsState()
	var title by remember { mutableStateOf("") }
	var genre by remember { mutableStateOf("") }
	var mood by remember { mutableStateOf("") }

	Scaffold(
		topBar = { TopAppBar(title = { Text("MovieLog") }) }
	) { padding ->
		Column(Modifier.padding(padding).padding(16.dp)) {
			OutlinedTextField(value = title, onValueChange = { title = it }, label = { Text("Название") })
			Spacer(Modifier.height(8.dp))
			OutlinedTextField(value = genre, onValueChange = { genre = it }, label = { Text("Жанр") })
			Spacer(Modifier.height(8.dp))
			OutlinedTextField(value = mood, onValueChange = { mood = it }, label = { Text("Настроение") })
			Spacer(Modifier.height(8.dp))
			Button(onClick = {
				if (title.isNotBlank()) {
					viewModel.addMovie(title.trim(), genre.trim(), mood.trim())
					title = ""; genre = ""; mood = ""
				}
			}) { Text("Сохранить") }

			Spacer(Modifier.height(16.dp))
			Text("Фильмы:", style = MaterialTheme.typography.titleMedium)
			LazyColumn {
				items(movies) { movie ->
					Text("• ${movie.title} — ${movie.genre} — ${movie.mood}")
				}
			}

			Spacer(Modifier.height(16.dp))
			Text("Статистика:", style = MaterialTheme.typography.titleMedium)
			val genreStats = viewModel.genreStats.collectAsState().value
			val moodStats = viewModel.moodStats.collectAsState().value
			Text("Жанры: " + genreStats.entries.joinToString { "${it.key}:${it.value}" })
			Text("Настроения: " + moodStats.entries.joinToString { "${it.key}:${it.value}" })
		}
	}
}
