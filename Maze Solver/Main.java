import java.util.* ;
import java.io.*   ;
class Node {

    Object item ;
    Node next   ;

    public Node ( Object Item , Node Next  ){

        item = Item ;
        next = Next ;

    }

}

class Point {
    int x ;
    int y ;
    int z ;

    public Point( int x , int y , int z ) {

        this.x = x ;
        this.y = y ;
        this.z = z ;

    }

}

interface IMazeSolver{

    public int[][]solveBFS(java.io.File maze) throws IOException ;

    public int[][]solveDFS(java.io.File maze) throws IOException ;

}

interface IQueue {

    public void enqueue(Object item) ;
    public Object dequeue() ;
    public boolean isEmpty() ;
    public int size() ;
    public void print() ;
    public void reverse() ;

}

interface IStack {

    public Object pop() ;
    public Object peek() ;
    public void push(Object item) ;
    public boolean isEmpty() ;
    public int size() ;
    public void print() ;

}

class LinkedListQueue implements IQueue {

    Node front , rear ;
    int size ;

    public LinkedListQueue() {

        front = rear = null ;
        size = 0 ;

    }

    @Override
    public void enqueue(Object item) {

        Node newNode = new Node( item , null ) ;

        if ( size == 0 )

            front = newNode ;

        else

            rear.next = newNode ;

        rear = newNode ;

        ++size ;

    }

    @Override
    public Object dequeue() {

        if ( isEmpty() )

            throw new RuntimeException() ;

        Object temp = front.item ;

        if ( size == 1 )

            front = rear = null ;

        else

            front = front.next ;

        --size ;

        return temp ;

    }

    @Override
    public boolean isEmpty() {

        return size == 0 ;

    }

    @Override
    public int size() {

        return size ;

    }

    @Override
    public void print() {

        System.out.print("[") ;

        Node current = front ;

        while ( current != null ) {

            System.out.print( current.item ) ;

            if ( current.next != null )

                System.out.print(", ") ;

            current = current.next ;

        }

        System.out.print("]") ;

    }

    public void reverse() {

        IStack stack = new MyStack() ;

        while ( front != null ) {

            stack.push( front ) ;
            front = front.next  ;

        }

        front = (Node) stack.pop() ;
        rear  = front ;

        while ( !stack.isEmpty() ) {

            rear.next = (Node) stack.pop() ;
            rear      = rear.next ;

        }

        rear.next = null ;

    }

}

class MyStack implements IStack {

    int length = 0 ;
    Node top   = null ;

    @Override
    public Object pop() {

        Node temp ;

        if ( isEmpty() )

            throw new RuntimeException() ;

        else {

            temp = top ;
            top  = top.next ;
            length-- ;

        }

        return temp.item ;

    }

    @Override
    public Object peek() {

        if ( isEmpty() )

            throw new RuntimeException() ;

        return top.item ;

    }

    @Override
    public void push( Object item ) {

        Node newNode = new Node( item , top ) ;
        top = newNode ;
        length++ ;

    }

    @Override
    public boolean isEmpty() {

        return length == 0 ;

    }

    @Override
    public int size() {

        return length ;

    }

    @Override
    public void print() {

        Node current = top ;
        System.out.print("[") ;

        while ( current != null ) {

            System.out.print( current.item ) ;

            if ( current.next != null )

                System.out.print(", ") ;

            current = current.next ;

        }

        System.out.print("]") ;

    }

}

class MazeSolver implements IMazeSolver {

    static boolean found_E = false ;

    static Point find_Start( char[][] Maze , int rows , int cols ) {

        Point Start = new Point( 0 , 0 , 0 ) ;

        for ( int i = 0 ; i < rows ; i++ ) {

            for ( int j = 0 ; j < cols ; j++ ) {

                if ( Maze[i][j] == 'S' ) {

                    Start.x = j ;
                    Start.y = i ;
                    Start.z = 1 ;

                    return Start ;

                }

            }

        }

        return Start ;

    }

    static boolean BFS( LinkedListQueue Queue , LinkedListQueue Queue_x , LinkedListQueue Queue_y , LinkedListQueue Queue_cost , char[][] Maze , int x , int y , int cost , int rows , int cols ) {

        if ( y < rows && y >= 0 && x < cols && x >= 0 ) {

            if ( Maze[y][x] == 'E' ) {

                Queue_x.enqueue(x) ;
                Queue_y.enqueue(y) ;
                Queue_cost.enqueue(cost) ;
                found_E = true  ;
                return true ;

            }

            if ( Maze[y][x] != '#' && Maze[y][x] != '+' ) {

                Maze[y][x] = '+' ;

                Queue_x.enqueue(x) ;
                Queue_y.enqueue(y) ;
                Queue_cost.enqueue(cost) ;

                Queue.enqueue( ( new Point( x , y , cost ) ) ) ;

            }

        }

        return false ;

    }

    static void DFS( MyStack Stack , LinkedListQueue Queue_x , LinkedListQueue Queue_y , LinkedListQueue Queue_cost , char[][] Maze , int x , int y , int cost , int rows , int cols ) {

        if ( y < rows && y >= 0 && x < cols && x >= 0 && !found_E ) {

            if ( Maze[y][x] == 'E' ) {

                Queue_x.enqueue(x) ;
                Queue_y.enqueue(y) ;
                Queue_cost.enqueue(cost) ;
                found_E = true ;

            }

            else if ( Maze[y][x] != '#' && Maze[y][x] != '+' ) {

                Maze[y][x] = '+' ;

                Queue_x.enqueue(x) ;
                Queue_y.enqueue(y) ;
                Queue_cost.enqueue(cost) ;

                Stack.push( ( new Point( x , y , cost ) ) ) ;

                DFS( Stack , Queue_x , Queue_y , Queue_cost , Maze ,    x     , y - 1 , cost + 1 , rows , cols) ;
                DFS( Stack , Queue_x , Queue_y , Queue_cost , Maze ,    x     , y + 1 , cost + 1 , rows , cols) ;
                DFS( Stack , Queue_x , Queue_y , Queue_cost , Maze ,    x - 1 , y     , cost + 1 , rows , cols) ;
                DFS( Stack , Queue_x , Queue_y , Queue_cost , Maze ,    x + 1 , y     , cost + 1 , rows , cols) ;

            }

        }

    }

    static int[][] find_path_BFS( LinkedListQueue Queue_cost , LinkedListQueue Queue_x , LinkedListQueue Queue_y , int cost ) {

        int[][] path = new int[cost][2];

        int current_cost = cost;

        boolean find = true ;

        Queue_x.reverse()    ;
        Queue_y.reverse()    ;
        Queue_cost.reverse() ;



        Queue_cost.dequeue() ;
        path[cost - 1][1] = (int) Queue_x.dequeue() ;
        path[cost - 1][0] = (int) Queue_y.dequeue() ;

        while (current_cost > 0 && !Queue_cost.isEmpty()){

            if(find){

                while ( (int)Queue_cost.front.item == current_cost){

                    Queue_cost.dequeue() ;
                    Queue_x.dequeue() ;
                    Queue_y.dequeue() ;

                }

                find = false ;
                current_cost -- ;

            }

            else {

                Queue_cost.dequeue() ;
                int x = (int) Queue_x.dequeue() ;
                int y = (int) Queue_y.dequeue() ;

                if( (x == path[current_cost][1] && (y - 1) == path[current_cost][0] ) || (x == path[current_cost][1] && (y + 1) == path[current_cost][0] ) || ( ( x - 1 )== path[current_cost][1] && y == path[current_cost][0] ) || ( ( x + 1 )== path[current_cost][1] && y == path[current_cost][0] )){

                    path[current_cost - 1][1] = x ;
                    path[current_cost - 1][0] = y ;
                    find = true ;

                }

            }

        }

        return path ;

    }

    static int[][] get_path_DFS( LinkedListQueue Queue_cost , LinkedListQueue Queue_x , LinkedListQueue Queue_y ) {

        Queue_x.reverse()    ;
        Queue_y.reverse()    ;
        Queue_cost.reverse() ;

        int step = 0     ;
        int current_cost ;

        int cost ;
        cost = (int) Queue_cost.front.item ;

        int[][] path = new int[cost][2] ;

        while ( !Queue_cost.isEmpty() ) {

            current_cost = (int) Queue_cost.dequeue() ;

            if ( current_cost == ( cost - step ) ) {


                path[cost - step - 1][1] = (int) Queue_x.dequeue() ;
                path[cost - step - 1][0] = (int) Queue_y.dequeue() ;
                step++ ;

            }

            else {

                Queue_x.dequeue() ;
                Queue_y.dequeue() ;

            }

        }

        return path ;

    }


    @Override
    public int[][] solveBFS( File maze ) throws IOException {

        BufferedReader br = new BufferedReader( new FileReader(maze) ) ;

        LinkedListQueue Queue      = new LinkedListQueue() ;
        LinkedListQueue Queue_x    = new LinkedListQueue() ;
        LinkedListQueue Queue_y    = new LinkedListQueue() ;
        LinkedListQueue Queue_cost = new LinkedListQueue() ;

        int x , y , South , North , East , West , cost = 1 ;

        Point Start , current ;

        String[] temp = br.readLine().split(" ") ;

        int rows = Integer.parseInt( temp[0] ) ;
        int cols = Integer.parseInt( temp[1] ) ;

        String Temp ;

        char[][] Maze = new char[rows][cols] ;

        for ( int i = 0 ; (Temp = br.readLine()) != null ; i++ ) {

            Maze[i] = Temp.toCharArray() ;

        }

        Start = find_Start( Maze , rows , cols ) ;

        Queue.enqueue( Start ) ;

        Queue_x.enqueue( Start.x)     ;
        Queue_y.enqueue( Start.y)     ;
        Queue_cost.enqueue( Start.z ) ;

        Maze[Start.y][Start.x] = '+'  ;

        while ( !Queue.isEmpty() ) {

            current = (Point) Queue.dequeue() ;

            x = current.x ;
            y = current.y ;
            cost = current.z + 1 ;

            South = y + 1 ;

            if ( BFS( Queue , Queue_x , Queue_y , Queue_cost , Maze , x , South , cost , rows , cols ) )

                break ;

            West = x - 1 ;

            if ( BFS( Queue , Queue_x , Queue_y , Queue_cost , Maze , West , y , cost , rows , cols ) )

                break ;

            North = y - 1 ;

            if ( BFS( Queue , Queue_x , Queue_y , Queue_cost , Maze , x , North , cost , rows , cols ) )

                break ;

            East = x + 1 ;

            if (BFS( Queue , Queue_x , Queue_y , Queue_cost , Maze , East , y , cost , rows , cols ) )

                break ;

        }

        if ( !found_E ) {

            System.out.println( "can't solve" ) ;
            return null ;

        }

        else

            return find_path_BFS( Queue_cost , Queue_x , Queue_y , cost ) ;

    }

    @Override
    public int[][] solveDFS(File maze) throws IOException {

        BufferedReader br = new BufferedReader( new FileReader(maze) ) ;

        MyStack stack = new MyStack() ;

        LinkedListQueue Queue_x    = new LinkedListQueue() ;
        LinkedListQueue Queue_y    = new LinkedListQueue() ;
        LinkedListQueue Queue_cost = new LinkedListQueue() ;

        int x , y , cost ;

        Point Start , current ;

        String[] temp = br.readLine().split(" ") ;

        int rows = Integer.parseInt( temp[0] ) ;
        int cols = Integer.parseInt( temp[1] ) ;

        String Temp ;

        char[][] Maze = new char[rows][cols] ;

        for ( int i = 0 ; ( Temp = br.readLine() ) != null ; i++ ) {

            Maze[i] = Temp.toCharArray() ;

        }

        Start = find_Start( Maze , rows , cols ) ;

        stack.push( Start ) ;

        while ( !stack.isEmpty() ) {

            current = (Point) stack.pop() ;
            x    = current.x ;
            y    = current.y ;
            cost = current.z ;


            DFS( stack , Queue_x , Queue_y , Queue_cost , Maze , x , y , cost , rows , cols ) ;

        }

        if ( !found_E ) {

            System.out.println("can't solve") ;
            return null ;

        }

        else

            return get_path_DFS( Queue_cost , Queue_x , Queue_y ) ;

    }

}

public class Main {

    static void print_maze(File maze, int[][] path) throws IOException {
        BufferedReader br = new BufferedReader( new FileReader(maze) ) ;


        String[] temp = br.readLine().split(" ") ;

        int rows = Integer.parseInt( temp[0] ) ;
        int cols = Integer.parseInt( temp[1] ) ;

        int spaces = Integer.toString(rows * cols).length() ;

        String Temp ;

        String[][] Maze = new String[rows][cols] ;

        for ( int i = 0 ; (Temp = br.readLine()) != null ; i++ ) {

            Maze[i] = Temp.split("") ;

        }

        for ( int i = 0 ; i < path.length ; i++){

            Maze[path[i][0]][path[i][1]] = Integer.toString(i + 1) ;

        }

        System.out.print(" ".repeat(spaces + 7));

        for (int i = 0 ; i < cols ; i++){
            System.out.print(i + " ".repeat(spaces - Integer.toString(i).length() + 1));
        }

        System.out.println();
        System.out.println(" ".repeat(spaces + 2) + "_".repeat(cols * (spaces + 1) + 7 ));
        System.out.println(" ".repeat(spaces + 1) + "|  " + "_".repeat(cols * (spaces + 1) + 3) + "  |");

        for (int i = 0 ; i < Maze.length ; i ++){

            System.out.print( i + " ".repeat(spaces - Integer.toString(i).length() + 1 ) + "| | ");
            System.out.print(" ".repeat(spaces - 1));

            for (int j = 0 ; j < Maze[0].length ; j++){

                System.out.print(Maze[i][j] + " ".repeat(spaces - Maze[i][j].length() + 1));

            }

                System.out.print("| |");
                System.out.println();

        }
        System.out.println(" ".repeat(spaces + 1) + "|  " + "-".repeat(cols * (spaces + 1) + 3) + "  |");
        System.out.println(" ".repeat(spaces + 2) + "-".repeat(cols * (spaces + 1) + 7 ));
    }
    static void print_path(int[][] path) {

        for ( int i = 0 ; i < path.length ; i++ ) {

            System.out.print("{") ; System.out.print(path[i][0]) ; System.out.print(",") ; System.out.print(" ") ; System.out.print(path[i][1]) ; System.out.print("}") ;

            if (i < path.length - 1)

                System.out.print(", ") ;

        }

    }

    public static void main(String[] args) throws IOException {

        /** Assumption that in DFS Direction is North - South - East - West **/

        try {

            Scanner in = new Scanner ( System.in ) ;

            int[][] path ;

            System.out.println("Enter the path of the file ") ;
            String path_file = in.nextLine() ;

            File file = new File(path_file) ;

            System.out.println("Enter the way to solve the maze ( Write BFS or DFS )");
            String way = in.nextLine() ;

            IMazeSolver Path = new MazeSolver() ;

            if ( Objects.equals( way , "BFS" ) )

                path = Path.solveBFS(file) ;

            else if ( Objects.equals( way , "DFS" ) )

                path = Path.solveDFS(file) ;

            else

                throw new RuntimeException() ;

            if ( path != null ) {
                print_maze(file, path);
                System.out.println();
                System.out.print("path: ");
                print_path(path);
            }

        } catch ( Exception e ){

            System.out.println("Error") ;

        }

    }

}