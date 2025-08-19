package com.example.movielog

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import androidx.room.*
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

@Entity(tableName = "movies")
data class Movie(
	@PrimaryKey(autoGenerate = true) val id: Int = 0,
	val title: String,
	val genre: String,
	val mood: String
)

@Dao
interface MovieDao {
	@Query("SELECT * FROM movies ORDER BY id DESC")
	fun getAll(): Flow<List<Movie>>

	@Insert
	suspend fun insert(movie: Movie)
}

@Database(entities = [Movie::class], version = 1)
abstract class AppDatabase : RoomDatabase() {
	abstract fun movieDao(): MovieDao
	companion object {
		@Volatile private var INSTANCE: AppDatabase? = null
		fun get(app: Application): AppDatabase =
			INSTANCE ?: synchronized(this) {
				INSTANCE ?: Room.databaseBuilder(app, AppDatabase::class.java, "movies.db").build().also { INSTANCE = it }
			}
	}
}

class MovieRepository(private val dao: MovieDao) {
	fun observeAll(): Flow<List<Movie>> = dao.getAll()
	suspend fun add(title: String, genre: String, mood: String) = dao.insert(Movie(title = title, genre = genre, mood = mood))
}

class MovieViewModel(app: Application) : AndroidViewModel(app) {
	private val repository = MovieRepository(AppDatabase.get(app).movieDao())
	val movies: StateFlow<List<Movie>> = repository.observeAll()
		.stateIn(viewModelScope, SharingStarted.Eagerly, emptyList())

	val genreStats: StateFlow<Map<String, Int>> = repository.observeAll()
		.map { list -> list.groupingBy { it.genre.ifBlank { "—" } }.eachCount() }
		.stateIn(viewModelScope, SharingStarted.Eagerly, emptyMap())

	val moodStats: StateFlow<Map<String, Int>> = repository.observeAll()
		.map { list -> list.groupingBy { it.mood.ifBlank { "—" } }.eachCount() }
		.stateIn(viewModelScope, SharingStarted.Eagerly, emptyMap())

	fun addMovie(title: String, genre: String, mood: String) {
		viewModelScope.launch {
			repository.add(title, genre, mood)
		}
	}
}
