#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <time.h>
#include <windows.h>
#include <fcntl.h>
#include <io.h>
#include <conio.h>
#include <string.h>

FILE* fp;
const player1 = 'X';
const player2 = 'O';
int n, m, top_player, Option, moves1, moves2, color1, color2, P1score, P2score, MenuSelection, t = 0, y = 1, slot ,flag_slot = 0,flag_turn ;
char Player1_name[100] , Player2_name[100] , path[500] = "D:\\Connect Four game\\parameters.xml";

typedef struct{
    char *name  ;
    char *score ;
} Player_information ;

Player_information player_information[10000] ;
Player_information distincit_player_information [10000];

typedef struct{
  int seconds;
  int minutes;
  int hours;
} Time;

Time my_time;

void SetColor(int ForgC)
{
  WORD wColor;
  // This handle is needed to get the current background attribute

  HANDLE hStdOut = GetStdHandle(STD_OUTPUT_HANDLE);
  CONSOLE_SCREEN_BUFFER_INFO csbi;
  // csbi is used for wAttributes word

  if (GetConsoleScreenBufferInfo(hStdOut, &csbi))
  {
    // To mask out all but the background attribute, and to add the color
    wColor = (csbi.wAttributes & 0xF0) + (ForgC & 0x0F);
    SetConsoleTextAttribute(hStdOut, wColor);
  }
  return;
}

void SpaceBoard(char board[n][m]){
  for(int i = 0; i < n; i++){
    for(int j = 0; j < m; j++){
      board[i][j] = ' ';
    }
  }
}

void save(int saveSlot, char board[n][m])
{

  FILE *fps;
  if (saveSlot == 1)
  {
    fps = fopen("save1.bin", "wb");
  }
  else if (saveSlot == 2)
  {
    fps = fopen("save2.bin", "wb");
  }
  else
  {
    fps = fopen("save3.bin", "wb");
  }
  for(int i = 0 ; i < n ; i++){

    for(int j = 0 ; j < m ; j++){

    fprintf(fps,"%c\n",board[i][j]);
}
}

  fclose(fps);
  FILE *saveSize;
  if (saveSlot == 1)
  {
    saveSize = fopen("saveSlot1.bin", "wb");
  }
  else if (saveSlot == 2)
  {
    saveSize = fopen("saveSlot2.bin", "wb");
  }
  else
  {
    saveSize = fopen("saveSlot3.bin", "wb");
  }
  fprintf(saveSize,"%d\n",n);
  fprintf(saveSize,"%d\n",m);
  fprintf(saveSize,"%d\n",color1);
  fprintf(saveSize,"%d\n",color2);
  fprintf(saveSize,"%d\n",moves1);
  fprintf(saveSize,"%d\n",moves2);
  fprintf(saveSize,"%d\n",flag_turn);
  fprintf(saveSize,"%d",Option);
  fclose(saveSize);
}

void load(int saveSlot, char board[n][m])
{
  int i = 0 ;
  int k = 0 ;
  char line[100][100] ;
  FILE *fpl;
  if (saveSlot == 1)
  {
    fpl = fopen("save1.bin", "r");
    if (fpl == NULL)
    {
      printf("couldn`t load returning to main menu\a\n");
      MainMenu();
    }
  }
  else if (saveSlot == 2)
  {
    fpl = fopen("save2.bin", "r");
    if (fpl == NULL)
    {
      printf("couldn`t load returning to main menu\a\n");
      MainMenu();
    }
  }
  else
  {
    fpl = fopen("save3.bin", "r");
    if (fpl == NULL)
    {
      printf("couldn`t load returning to main menu\a\n");
      MainMenu();
    }
  }
   while (fgets(line[i], 100, fpl))
  {
    i++;
  }

  for(int l = 0 ; l < n ; l++){
    for(int j = 0 ; j < m ; j++){
        board[l][j] = line[k][0] ;
        k++;
    }
  }

fclose(fpl);
  }

void PrintBoard(char board[n][m])
{
  for (int k = 0; k < m; k++)
  {
    SetColor(1);
    printf(" _____ ");
  }
  printf("\n");
  for (int i = 0; i < n; i++)
  {
    for (int l = 0; l < m; l++) /////////////////////////&n,m
    {
      SetColor(1);
      printf("|     |");
    }
    printf("\n");
    for (int j = 0; j < m; j++)
    {
      SetColor(1);
      printf("|  ");
      if (board[i][j] == 'X')
        SetColor(color1);
      else
        SetColor(color2);
      if (board[i][j] != ' ')
      {
        SetConsoleOutputCP(CP_UTF8);
        printf("%s", "●");
        SetColor(1);
        printf("  |");
      }
      else
      {
        SetColor(1);
        printf("   |");
      }
    }
    printf("\n");
    for (int l = 0; l < m; l++)
    {
      SetColor(1);
      printf("|_____|");
    }
    printf("\n");
  }
}

void Player_move(char board[n][m], int location[n*m*2]  , char player)
{
  int chosen_col, flag = 0, i = 0;

  do
  {
    if (i)
      printf("\a");

    SetColor(255);
    printf("\nPlease choose your column: \n");
    scanf("%d", &chosen_col);
    i++;

  } while ((chosen_col <= 0) || (chosen_col > m));
  do
  {

    chosen_col--;

    for (int i = n - 1; i >= 0; i--)
    {
      if (board[i][chosen_col] == ' ')
      {
        board[i][chosen_col] = player;
        location[t] = i ;
        location[y] = chosen_col ;
        t+=2;
        y+=2;

        if (player == 'X')
        {
          moves1++;
        }

        else if (player == 'O')
        {
          moves2++;
        }

        flag = 1;
        break;
      }
    }

    if (flag == 0)
    {
      printf("\a");
      printf("\nPlease choose your column: \n");
      scanf("%d", &chosen_col);
    }

  } while (flag == 0);
}

int Check_Free_Spaces(char board[n][m])
{
  int freeSpaces = n * m;

  for (int i = 0; i < n ; i++)
  {
    for (int j = 0; j < m; j++)
    {
      if (board[i][j] != ' ')
      {
        freeSpaces--;
      }
    }
  }
  return freeSpaces;
}

void computerMove(char board[n][m] , int location[n*m*2] )
{
  // creates a seed based on current time
  srand(time(0));
  int x2;
  int x1;
  int flag = 0;

  if (Check_Free_Spaces(board) > 0)
  {

    do
    {
      x2 = rand() % m ;
      for (x1 = (n - 1); x1 >= 0; x1--)
      {
        if (board[x1][x2] == ' ')
        {
          board[x1][x2] = player2;
          location[t] = x1 ;
          location[y] = x2 ;
          t+=2;
          y+=2;
          moves2++;
          flag = 1;
          break;
        }
      }
    } while (flag == 0);
  }
}

void User_Rank()
{
  char line[100][100];
  int  name  =  0 ;
  int  score =  1 ;
  int  num_of_player_and_score =  0 ;
  int  num_of_dist_player = 0 ;
  int  value  ;
  FILE *rank  ;

  rank = fopen("rank.bin", "r");

  while (fgets(line[num_of_player_and_score], 100, rank))
  {
    line[num_of_player_and_score][strlen(line[num_of_player_and_score]) - 1] = '\0';
    num_of_player_and_score++;
  }

  for ( int i = 0 ; i < (num_of_player_and_score / 2) ; i++ )
  {
    player_information[i].name = line[name];
    player_information[i].score = line[score];
    name  += 2;
    score += 2;
  }

  fclose(rank);

  char *temp1;
  char *temp2;
  for (int a = 0; a < num_of_player_and_score / 2; a++)
  {
    for (int b = 0; b < num_of_player_and_score / 2 - 1; b++)
    {
      if ( strcmp(player_information[b].score , player_information[a].score ) < 0)
      {
        temp1 = player_information[b].score;
        player_information[b].score = player_information[a].score;
        player_information[a].score = temp1;
        temp2 = player_information[b].name;
        player_information[b].name = player_information[a].name;
        player_information[a].name = temp2;
      }
    }
  }

  for (int i = 0 ;  i < num_of_player_and_score / 2; i++)
  {
    for (int j = i + 1 ; j < num_of_player_and_score / 2 ; j++)
    {
      value = strcmp(player_information[i].name, player_information[j].name);

      if (value == 0)
      player_information[j].name = " ";

    }
  }

  for (int i = 0 ; i < num_of_player_and_score / 2 ; i++)
  {
    if (player_information[i].name != " ")
    {
      distincit_player_information[num_of_dist_player].name  = player_information[i].name;
      distincit_player_information[num_of_dist_player].score = player_information[i].score;
      num_of_dist_player++;
    }
  }

  int permutation;

  if ( num_of_dist_player < top_player )
  {
    permutation = num_of_dist_player;
  }
  else
  {
    permutation = top_player;
  }
    printf("                 ***************\n");
    printf("                 * top players *\n");
    printf("                 ***************\n\n");
    for ( int x = 0 ; x < permutation ; x++)
  {
    printf("%d # %s score %s\n", x + 1, distincit_player_information[x].name, distincit_player_information[x].score);
  }
}

int checkpoint_player(char board[n][m], char player)
{
  int score = 0;
  char board_row[n][m];
  char board_column[n][m];
  char board_diagonal_1[n][m];
  char board_diagonal_2[n][m];

  for (int i = 0; i < n; i++)
  {
    for (int j = 0; j < m; j++)
    {
      board_diagonal_1[i][j] = board[i][j];
      board_diagonal_2[i][j] = board[i][j];
      board_column[i][j] = board[i][j];
      board_row[i][j] = board[i][j];
    }
  }
  // check rows
  for (int i = 0; i < n; i++)
  {
    for (int j = 0; j <= m - 4; j++)
    {
      if (board_row[i][j] == player && board_row[i][j + 1] == player && board_row[i][j + 2] == player && board_row[i][j + 3] == player)
      {
        score++;
        board_row[i][j] = '0';
        board_row[i][j + 1] = '0';
        board_row[i][j + 2] = '0';
        board_row[i][j + 3] = '0';
      }
    }
  }
  // check columns
  for (int i = 0; i < m; i++)
  {
    for (int j = 0; j <= n - 4; j++)
    {
      if (board_column[j][i] == player && board_column[j + 1][i] == player && board_column[j + 2][i] == player && board_column[j + 3][i] == player)
      {
        score++;
        board_column[j][i] = '0';
        board_column[j + 1][i] = '0';
        board_column[j + 2][i] = '0';
        board_column[j + 3][i] = '0';
      }
    }
  }
  // check diagonals_1
  for (int i = 0; i < n - 3; i++)
  {
    for (int j = 0; j < m; j++)
    {
      if (j + 4 > m)
      {
        break;
      }
      if (board_diagonal_1[i][j] == player && board_diagonal_1[i + 1][j + 1] == player && board_diagonal_1[i + 2][j + 2] == player && board_diagonal_1[i + 3][j + 3] == player)
      {
        score++;
        board_diagonal_1[i][j] = '0';
        board_diagonal_1[i + 1][j + 1] = '0';
        board_diagonal_1[i + 2][j + 2] = '0';
        board_diagonal_1[i + 3][j + 3] = '0';
      }
    }
  }
  // check diagonals_2
  for (int i = n - 1; i >= 3; i--)
  {
    for (int j = 0; j < m; j++)
    {
      if (j + 4 > m)
      {
        break;
      }
      if (board_diagonal_2[i][j] == player && board_diagonal_2[i - 1][j + 1] == player && board_diagonal_2[i - 2][j + 2] == player && board_diagonal_2[i - 3][j + 3] == player)
      {
        score++;
        board_diagonal_2[i][j] = '0';
        board_diagonal_2[i - 1][j + 1] = '0';
        board_diagonal_2[i - 2][j + 2] = '0';
        board_diagonal_2[i - 3][j + 3] = '0';
      }
    }
  }
  return score;
}

void GamePeriod(long int secs)
{
  my_time.hours = secs / 3600;

  my_time.minutes = (secs - my_time.hours * 3600) / 60;

  my_time.seconds = (secs) - (my_time.hours * 3600) - (my_time.minutes * 60);

  printf("\nTime passed : %d:%d:%d \n\n", my_time.hours, my_time.minutes, my_time.seconds);
}
void CreatingColors()
{
  srand(time(0));
  do
  {
    color1 = rand() % 8;
    color2 = rand() % 8;

  } while (color1 == 0 || color2 == 0 || color1 == color2 || color1 == 1 || color2 == 1);
}

void GettingParameters()
{
  char file[2048];

  fp = fopen(path, "r");

  fseek(fp, 0, SEEK_END);                                       // pointer goes to the end of file
  int length = ftell(fp);                                       // gives the current position so it indicates number of chars in file
  fseek(fp, 0, SEEK_SET);                                       // brings the pointer back to start
  char *lowSpacelessFile = malloc(sizeof(char) * (length + 1)); // freeeeeeeee
  char c;
  int i = 0;
  while (((c = fgetc(fp)) != EOF))
  {
    if ((c != ' ') && (c != '\n') && (c != '\t'))
    {
      lowSpacelessFile[i] = tolower(c);
      i++;
    }
    else
    {
      continue;
    }
  }

  fclose(fp);

  char *pconfg1 = strstr(lowSpacelessFile, "<configurations>");
  char *pconfg2 = strstr(lowSpacelessFile, "</configurations>");
  char *ph1 = strstr(lowSpacelessFile, "<height>");
  char *ph2 = strstr(lowSpacelessFile, "</height>");
  char *pw1 = strstr(lowSpacelessFile, "<width>");
  char *pw2 = strstr(lowSpacelessFile, "</width>");
  char *ps1 = strstr(lowSpacelessFile, "<highscores>");
  char *ps2 = strstr(lowSpacelessFile, "</highscores>");

  // getting height
  ph1 += 8;
  i = 0;
  char Harr[10];
  for (ph1; ph1 < ph2; ph1++)
  {
    Harr[i++] = *ph1;
  }

  n = atoi(Harr);
  // printf("%d\n", height);
  //  getting width
  pw1 += 7;
  i = 0;
  char Warr[10];

  for (pw1, i = 0; pw1 < pw2; pw1++)
  {
    Warr[i++] = *pw1;
  }

  m = atoi(Warr);
  // getting number of high scores
  ps1 += 12;
  i = 0;
  char Sarr[10];

  for (ps1; ps1 < ps2; ps1++)
  {
    Sarr[i++] = *ps1;
  }

  top_player = atoi(Sarr);
}

void CreatingBoard()
{
  int pathTrials = 2;
  GettingParameters();
  while ((fp == NULL) || (n < 4) || (m < 4) || (top_player <= 0))
  {
    if (pathTrials > 0)
    {
      printf("\ncorrupted data\a\n\n");
      printf("please enter a path without double quotes: ");
      fflush(stdin);
      gets(path);
      GettingParameters();
      pathTrials--;
    }
    else
    {
      printf("\nfailed to get parameters from user\a\n\nSetting Default Parameters Height:7 Width:9 HighScores:10 \a\n");
      n = 7;
      m =  9;
      top_player = 10;
      break;
    }
  }
}


int ChoosingGameMode()
{
  do
  {
    printf("\nChoose your game mode : \npress 1 for (player vs player)\npress 2 for (player vs comp)\n");

    scanf("%d", &Option);

  } while (Option != 1 && Option != 2);
  return Option;
}

void Match(char board[n][m], int location[n*m*2] , char player , int color , int moves , long int start ){

printf("\n");
  if( Option == 1 ){
          char x ;

      SetColor(color);

     if ( player == player1 ){
          printf("Player 1 turn \n\n");
          flag_turn = 1 ;
     }

      else{
          printf("Player 2 turn \n\n");
          flag_turn = 2 ;
     }

   while (Check_Free_Spaces(board) != 0)
   {

   do{
        printf("press : (u) to undo\n");
        printf("press : (r) to redo\n");
        printf("press : (s) to save the game\n");
        printf("press : (q) to quit the game\n");
        printf("press : (any thing else) to choose coloumn\n");
        SetColor(15);
        scanf("%c" ,&x);
        scanf("%c" ,&x);
        SetColor(color);
    if( t <= 0 && x == 'u' ){
            printf("\ncan't make undo\n\n\a");
    }

    else if( location[t] == ' ' && x == 'r'){
            printf("\ncan't make redo\n\n\a");
    }

   }while( x =='u' && t <= 0 || x =='r' && location[t] == ' ' );
   if( x == 'u' && t >= 0 ){

       if( player == player1 )
       {
          moves2 -- ;
          moves = moves2 ;
          color = color2 ;
          SetColor(color);
       }

       else{
          moves1 -- ;
          moves = moves2 ;
          color = color1 ;
          SetColor(color);
       }

          t-=2 ;
          y-=2 ;
          board[location[t]][location[y]] = ' ';
          PrintBoard(board);
          SetColor(color);
          printf("\nPlayer moves: %d\n", moves);
          printf("Player score: %d\n", checkpoint_player(board, player) );
          time_t end = time(NULL);
          long int secs = difftime(end , start) ;
          GamePeriod(secs);

     }

       else if ( x == 'r' && location[t] != ' ' ){

       if( player == player1 )
       {
          moves1 ++ ;
          moves = moves1 ;
          color = color2 ;
          SetColor(color);
       }

       else{
          moves2 ++ ;
          moves = moves2 ;
          color = color1 ;
          SetColor(color);
       }

          board[location[t]][location[y]] = player ;
          t+=2 ;
          y+=2 ;
          PrintBoard(board);

          SetColor(color);
          printf("\nPlayer moves: %d\n", moves);
          printf("Player score: %d\n", checkpoint_player(board, player) );
          time_t end = time(NULL);
          long int secs = difftime(end , start) ;
          GamePeriod(secs);
       }

       else if (x == 'q'){
        SetColor(15);
        printf("\nquiting connect 4\n\n");
        printf("enter any thing to quit game");
        SetColor(0);
        exit(0);

       }
       else if(x == 's'){
        SetColor(15);
        printf("\nenter the slot : ");
        scanf("%d" ,&slot );
        printf("Saved Successfully\n\n");
        save(slot ,board);
       }

        else{

         for (int i = t+1 ; i < n*m*2 ; i++ ){
            location[i] = ' ' ;
         }

         PrintBoard(board);
         SetColor(color);
         printf("\nPlayer moves: %d\n", moves);
         printf("Player Score: %d\n", checkpoint_player(board , player) );
         Player_move(board,location , player);
         time_t end = time(NULL);
         long int secs = difftime(end, start);
         GamePeriod(secs);
         PrintBoard(board);
         SetColor(color);
        }
        if( player == player1){
           moves  = moves2  ;
           color  = color2  ;
           player = player2 ;

        }
        else {
            moves  = moves1  ;
            color  = color1  ;
            player = player1 ;

        }
         Match(board , location , player ,  color , moves , start);
   }
  }
   if( Option == 2){
     char x ;
     SetColor(color);
           if (player == player1 ){

              printf("Player turn \n");
              flag_turn = 1 ;
           }
           else{

              printf("Computer turn \n");
              flag_turn = 2 ;

           }

      while (Check_Free_Spaces(board) != 0)
      {

       do{
        printf("press : (u) to undo\n");
        printf("press : (r) to redo\n");
        printf("press : (s) to save the game\n");
        printf("press : (q) to quit the game\n");
        printf("press : (any thing else) to choose coloumn\n");
       SetColor(15);
       scanf("%c" ,&x);
       scanf("%c" ,&x);
       SetColor(color);
       if( t <= 0 && x == 'u' ){
        printf("\ncan't make undo\n");
         }

    else if( location[t+2] == ' ' && x == 'r'){
            printf("\ncan't make redo\n");
         }

   }while( x =='u' && t <= 0 || x =='r' && location[t] == ' ' );

     if( x == 'u' && t >= 0 ){
         if( player == player1 )
       {
          moves2 -- ;
          moves = moves2;
          color = color2 ;
          SetColor(color);
          printf("Computer turn\n");
       }

       else{
          moves1 -- ;
          moves = moves1 ;
          color = color1 ;
          SetColor(color);
          printf("Player turn\n");
       }

          t-=2 ;
          y-=2 ;
          board[location[t]][location[y]] = ' ';

          PrintBoard(board);
          SetColor(color);
          printf("\nPlayer moves: %d\n", moves);
          printf("Player score: %d\n", checkpoint_player(board, player) );
          time_t end = time(NULL);
          long int secs = difftime(end , start) ;
          GamePeriod(secs);
        }

        else if ( x == 'r' && location[t+2] != ' ' ){

           if( player == player1 )
       {
          moves1 ++ ;
          moves = moves1;
          color = color2 ;
          SetColor(color);
          printf("computer turn\n");
       }

       else{
          moves2 ++ ;
          moves = moves2 ;
          color = color1 ;
          SetColor(color);
          printf("Player turn\n");
       }


         board[location[t]][location[y]] = player ;
          t+=2 ;
          y+=2 ;

          if ( player == player1 ){
            board[location[t]][location[y]] = player2 ;
          }

          else{
            board[location[t]][location[y]] = player1 ;
          }

          PrintBoard(board);
          SetColor(color);
          printf("\nPlayer moves: %d\n", moves);
          printf("Player score: %d\n", checkpoint_player(board, player) );
          time_t end = time(NULL);
          long int secs = difftime(end , start) ;
          GamePeriod(secs);
       }

       else if (x == 'q'){
        SetColor(15);
        printf("\nquiting connect 4\n\n");
        printf("enter any thing to quit game");
        SetColor(0);
        exit(0);

       }
       else if(x == 's'){
        SetColor(15);
        printf("\nenter the slot : ");
        scanf("%d" ,&slot );
        printf("Saved Successfully\n\n");
        save(slot ,board);
       }

        else{

         for (int i = t+1 ; i < n*m*2 ; i++ ){
            location[i] = ' ' ;
         }

         PrintBoard(board);
         SetColor(color);
         printf("\nPlayer moves: %d\n", moves);
         printf("Player Score: %d\n", checkpoint_player(board , player) );
         if (player == player1){
            Player_move(board,location , player);
         }

         else{
         computerMove(board ,location);
         }

         time_t end = time(NULL);
         long int secs = difftime(end, start);
         GamePeriod(secs);
         PrintBoard(board);
         SetColor(color);
         }
         if( player == player1){
           moves  = moves2  ;
           color  = color2  ;
           player = player2 ;
         }

        else {
            moves  = moves1  ;
            color  = color1  ;
            player = player1 ;

        }
         Match(board , location , player ,  color , moves , start);

   }
  }
 }

void MatchResult(char board[n][m])
{
    P1score = checkpoint_player(board,player1);
    P2score = checkpoint_player(board,player2);

  if (P1score > P2score)
  {
    SetColor(color1);
    printf("Player 1 Won! (%d : ",P1score);
    SetColor(color2);
    printf("%d)\n\n",P2score);
  }
  else if (P1score < P2score)
  {
    if (Option == 1)
    {
      SetColor(color2);
      printf("Player 2 Won! (");
      SetColor(color1);
      printf("%d ",P1score);
      SetColor(color2);
      printf(": %d)\n\n",P2score);
    }

    else if (Option == 2)
    {
      SetColor(color2);
      printf("Computer Won! (");
      SetColor(color1);
      printf("%d ",P1score);
      SetColor(color2);
      printf(": %d)\n\n",P2score);
    }
  }

  else if(P1score == P2score)
  {
    SetColor(color1);
    printf("IT`S A ");
    SetColor(color2);
    printf("DRAW! ");
    SetColor(color1);
    printf("(%d :",P1score);
    SetColor(color2);
    printf(" %d)\n\n",P2score);

  }
}
void Play()
{

  int color , moves ;
  char player ;
  if (flag_slot == 1){

    int i = 0 ;
    int arr[100] ;
    int input[100];
    FILE*load_slot ;
    if(slot == 1){

        load_slot = fopen("saveSlot1.bin","r");
    }
    else if(slot == 2){

        load_slot = fopen("saveSlot2.bin","r");
    }
    else if(slot == 3){

        load_slot = fopen("saveSlot3.bin","r");
    }

  while (fgets(arr, 100 ,load_slot))
  {
    input[i]= atoi(arr);
    i++ ;
  }

  n = input[0];
  m = input[1];
  color1 = input[2];
  color2 = input[3];
  moves1 = input[4];
  moves2 = input[5];
  flag_turn =input[6];
  Option =input[7] ;
  fclose(load_slot);
  }
  char board[n][m] ;

  if( flag_slot == 1 ){

    load(slot, board);
    if(flag_turn ==1 ){

        color =color1 ;
        player = player1 ;
        moves = moves1 ;
    }
    if(flag_turn ==2 ){

        color =color2 ;
        player = player2 ;
        moves = moves2 ;
    }

  }

  else{
    CreatingColors()   ;
    ChoosingGameMode() ;
    SpaceBoard(board)  ;
    color = color1 ;
    moves = moves1 ;
    player =player1 ;

  }
  time_t start = time(NULL);
  int location[n*m*2] ;

  for (int i = 0 ; i <n*m*2 ; i++){
    location[i] = ' ';
  }
  t = 0 ;
  y = 1 ;
  moves1 = 0 ;
  moves2 = 0 ;

  Match(board , location , player , color , moves , start);
  MatchResult(board);
}
void MainMenu()
{
  CreatingBoard() ;

  printf("\n");
  printf("                       ***************************\n");
  printf("                       *   Welcome To Connect-4  *\n");
  printf("                       ***************************\n\n");
  do
  {
    printf(" **************\n");
    printf(" *  MAIN MENU *\n");
    printf(" **************\n\n");
    printf("enter 1 to: play a new game\n");
    printf("enter 2 to: load a game\n");
    printf("enter 3 to: top player\n");
    printf("enter 4 to: exit the game\n");
    scanf("%d", &MenuSelection);
  } while (MenuSelection != 1 && MenuSelection != 2 && MenuSelection != 3 && MenuSelection != 4 && isalpha(MenuSelection));

  Game();
}
void Game()
{
  switch (MenuSelection)
  {
  case 1:
    Play();
   if (Option == 1){
    SetColor(color1);
    printf("Please, Enter the name of player 1:  ");
    fflush(stdin);
    gets(Player1_name);
    SetColor(color2);
    printf("Please, Enter the name of player 2:  ");
    fflush(stdin);
    gets(Player2_name);
   }
   else {
    printf("Please , Enter your name:  ");
    fflush(stdin);
    gets(Player1_name);
   }

  FILE*rank ;
  rank = fopen("rank.bin","a");
   if(Option == 1){
     for(int i = 0 ; i < strlen(Player1_name);i++)
  {
      Player1_name[i]=tolower(Player1_name[i]);
  }

  for(int i = 0;i<strlen(Player2_name);i++)
  {
      Player2_name[i]=tolower(Player2_name[i]);
  }

   fprintf(rank , "%s\n" , Player1_name );
   fprintf(rank , "%d\n" , P1score);
   fprintf(rank , "%s\n" , Player2_name );
   fprintf(rank , "%d\n" , P2score);
   }
   else{
   for(int i = 0 ; i < strlen(Player1_name);i++)
  {
      Player1_name[i]=tolower(Player1_name[i]);
  }
   fprintf(rank , "%s\n" , Player1_name );
   fprintf(rank , "%d\n" , P1score ) ;
   }
   fclose(rank);

    int inGameChoice;
    do
    {
      SetColor(15);

      moves1 = 0 ;
      moves2 = 0 ;

      printf("\nenter 1 to play again\n");
      printf("enter 2 to return to Main Menu\n");

      scanf("%d", &inGameChoice);
    } while (inGameChoice != 1 && inGameChoice != 2);
    if (inGameChoice == 1)
    {
      Game();
    }
    else if (inGameChoice == 2)
    {
      MainMenu();
    }

    break;

    case 2:
      flag_slot = 1 ;
      printf("\nenter the number of slot : ");
      scanf("%d" , &slot ) ;
      Play();
      flag_slot = 0 ;

      break;
     case 3 :
     User_Rank();
     MainMenu();
     break;
    case 4:
    printf("\nQuitting Connect-4\n\n");
    printf("press any thing to quit");
    SetColor(0);
    exit(0);
   }
 }

int main()
{
  MainMenu();
  getch();
  return 0;
}

