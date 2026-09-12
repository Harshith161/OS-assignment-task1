package matrix;

public class MatMulCellThreads {
    static int a[][] = {{2,3},{4,1},{6,5}};
    static int b[][] = {{1,4,2},{3,2,5}};
    static int res[][] = new int[3][3];

    static class CellWorker extends Thread {
        int row, col;
        CellWorker(int row, int col){
            this.row = row;
            this.col = col;
        }
        public void run(){
            int sum = 0;
            for(int k = 0; k < b.length; k++){
                sum += a[row][k] * b[k][col];
            }
            res[row][col] = sum;
        }
    }

    public static void main(String args[]) throws Exception {
        int rows = a.length;
        int cols = b[0].length;
        CellWorker workers[][] = new CellWorker[rows][cols];

        for(int i = 0; i < rows; i++){
            for(int j = 0; j < cols; j++){
                workers[i][j] = new CellWorker(i, j);
                workers[i][j].start();
            }
        }

        for(int i = 0; i < rows; i++){
            for(int j = 0; j < cols; j++){
                workers[i][j].join();
            }
        }

        for(int[] row : res){
            for(int val : row) System.out.print(val + "\t");
            System.out.println();
        }
    }
}