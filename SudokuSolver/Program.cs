using System;

namespace SudokuSolver
{
    class Program
    {
        internal SudokuItem[,] board;
        internal int row;
        internal int col;
        internal int boardSolved;
        internal int maxValue;
        static void Main(string[] args)
        {
            int[,] newBoard = new int[9, 9] { { 0,3,1,0,0,0,4,0,0},
                                              { 0,4,0,0,0,0,0,5,2},
                                              { 0,0,0,5,0,0,0,0,0},
                                              { 0,0,6,1,0,0,2,0,0},
                                              { 0,1,0,3,0,6,0,0,0},
                                              { 7,0,0,2,0,0,0,9,1},
                                              { 9,0,0,0,0,0,0,7,0},
                                              { 0,0,0,0,6,0,0,0,0},
                                              { 0,0,0,9,0,8,0,0,5} };
            Program p = new Program();
            Console.WriteLine(p.SolveBoard(newBoard).ToString());
        }

        internal int SolveBoard(int[,] arr)
        {
            InitializeBoard(arr);
            boardSolved = 0;
            row = 0;
            col = 0;
            maxValue = board.GetLength(0);
            if (board[0, 0].Value != 0)
            {
                Increment();
            }
            while (boardSolved == 0)
            {
                board[row, col].Value = GetNextVal();
                if (board[row, col].Value == 0)
                {
                    Decrement();
                }
                else
                {
                    Increment();
                }
            }
            for (int i = 0; i < board.GetLength(0); i++)
            {
                for (int j = 0; j < board.GetLength(0); j++)
                {
                    Console.Write(board[i,j].Value);
                }
                Console.Write("\n");
            }
            return boardSolved;
        }

        internal int GetNextVal()
        {
            if (board[row, col].MinValue > maxValue)
            {
                board[row, col].MinValue = 1;
                return 0;
            }
            for (int i = board[row, col].MinValue; i < board.GetLength(0) + 1; i++)
            {
                if (IsValid(i))
                {
                    board[row, col].MinValue = i + 1;
                    return i;
                }
            }
            board[row, col].MinValue = 1;
            return 0;
        }

        internal bool IsValid(int val)
        {
            for (int i = 0; i < board.GetLength(0); i++)
            {
                if (board[row, i].Value == val)
                {
                    return false;
                }
            }
            for (int i = 0; i < board.GetLength(0); i++)
            {
                if (board[i, col].Value == val)
                {
                    return false;
                }
            }
            int tempRow, tempCol;
            if (row % 3 == 0)
            {
                tempRow = row;
            }
            else if (row % 3 == 1)
            {
                tempRow = row - 1;
            }
            else
            {
                tempRow = row - 2;
            }
            if (col % 3 == 0)
            {
                tempCol = col;

            }
            else if (col % 3 == 1)
            {
                tempCol = col - 1;
            }
            else
            {
                tempCol = col - 2;
            }
            if (board[tempRow, tempCol].Value == val || board[tempRow + 1, tempCol].Value == val || board[tempRow + 2, tempCol].Value == val ||
                board[tempRow, tempCol + 1].Value == val || board[tempRow + 1, tempCol + 1].Value == val || board[tempRow + 2, tempCol + 1].Value == val ||
                board[tempRow, tempCol + 2].Value == val || board[tempRow + 1, tempCol + 2].Value == val || board[tempRow + 2, tempCol + 2].Value == val)
            {
                return false;
            }
            return true;
        }

        internal void Decrement()
        {
            if (col > 0)
            {
                col--;
            }
            else if (row > 0)
            {
                row--;
                col = board.GetLength(0)-1;
            }
            else
            {
                boardSolved = -1; //unable to solve
            }
            if (board[row, col].IsLocked)
            {
                Decrement();
            }
        }

        internal void Increment()
        {
            if (col < board.GetLength(0) - 1)
            {
                col++;
            }
            else if (row < board.GetLength(1) - 1)
            {
                row++;
                col = 0;
            }
            else
            {
                boardSolved = 1;
                return;
            }
            if (board[row, col].IsLocked)
            {
                Increment();
            }
        }

        internal void InitializeBoard(int[,] arr)
        {
            board = new SudokuItem[arr.GetLength(0), arr.GetLength(1)];
            for (int i = 0; i < arr.GetLength(0); i++)
            {
                for (int j = 0; j < arr.GetLength(1); j++)
                {
                    if (arr[i, j] != 0)
                    {
                        board[i, j] = new SudokuItem { Value = arr[i, j], IsLocked = true, MinValue = 0 };
                    }
                    else
                    {
                        board[i, j] = new SudokuItem { Value = arr[i, j], IsLocked = false, MinValue = 1 };
                    }
                }
            }
        }

        internal class SudokuItem
        {
            internal int Value { get; set; }
            internal bool IsLocked { get; set; }
            internal int MinValue { get; set; }
        }
    }
}
