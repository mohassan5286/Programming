package routh.example;

import java.util.Arrays;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.apache.commons.math3.analysis.polynomials.PolynomialFunction;
import org.apache.commons.math3.analysis.solvers.LaguerreSolver;
import org.apache.commons.math3.complex.Complex;
import java.util.HashMap;
import java.util.Map;


public class RouthCriteria {

    public static void main(String[] args) {
        Scanner ip = new Scanner(System.in);
        System.out.print("Enter the characteristic equation: ");
        String input = ip.nextLine().replaceAll("\\s+", ""); // Remove whitespace for easier parsing
        ip.close();

        // Define a pattern to match coefficients and powers
        Pattern pattern = Pattern.compile("(-?\\d*)\\*?s\\^(\\d+)|(-?\\d+)\\*?s|(-?\\d+)");

        // Initialize a map to store coefficients for each power
        Map<Integer, Double> coefficientMap = new HashMap<>();

        // Find the maximum power to initialize the coefficient array
        int maxPower = 0;
        Matcher matcher = pattern.matcher(input);
        while (matcher.find()) {
            String coefficientStr = matcher.group(1) != null ? matcher.group(1) :
                    (matcher.group(3) != null ? matcher.group(3) :
                            (matcher.group(4) != null ? matcher.group(4) : "1")); // Default to 1 if no coefficient is specified
            String powerStr = matcher.group(2) != null ? matcher.group(2) :
                    (matcher.group(3) != null ? "1" :
                            (matcher.group(4) != null ? "0" : "0")); // Default to 0 if no power is specified

            double coefficient = coefficientStr.isEmpty() ? 1.0 : Double.parseDouble(coefficientStr);
            int power = Integer.parseInt(powerStr);
            coefficientMap.put(power, coefficient);

            if (power > maxPower) {
                maxPower = power;
            }
        }

        // Create the coefficient array with correct signs and order
        double[] coeffArray = new double[maxPower + 1];
        for (int i = 0; i <= maxPower; i++) {
            coeffArray[i] = coefficientMap.getOrDefault(i, 0.0);
        }

        Double[][] routhArray = constructRouthArray(maxPower, coeffArray);

        System.out.println("Routh Array:");
        for (Double[] row : routhArray) {
            System.out.println(Arrays.toString(row));
        }

        int numOFsignchanges = countSignChanges(routhArray);
        if (numOFsignchanges > 0) {
            System.out.println("The system is unstable with " + numOFsignchanges + " poles in RHS");
        } else {
            System.out.println("The system is stable");
        }

        Complex[] roots = findRoots(coeffArray);
        System.out.println("Roots:");
        for (Complex root : roots) {
            double real = root.getReal();
            double imag = root.getImaginary();

            if (imag == 0) {
                System.out.printf("Root: %.2f\n", real);
            } else {
                System.out.printf("Root: %.2f %s %.2fi\n", real, imag > 0 ? "+" : "-", Math.abs(imag));
            }
        }


    }

    private static Double[][] constructRouthArray(int maxPower , double[] coefficients) {
        int temp1 = maxPower;
        int count =0;
        while (temp1 >= 0) {
            temp1 = temp1 -2;
            count++;
        }
        int n = coefficients.length;
        int m = count;;
        Double[][] routhArray = new Double[n][m];
        for (int i=0 ;i<n ;i++)
        {
            for (int j=0 ;j<m ;j++)
            {
                routhArray[i][j] = null; //any number to intialize
            }
        }
        for (int i =0 ;i<2 ; i++)
        {
            int k = 0;
            for (int j=0 ; j<m ; j++)
            {
                int pp = n - 1 - i - k;
                if (pp >= 0){
                    double temp2 = coefficients[pp];
                    routhArray[i][j] = temp2;
                    k += 2;}
            }
        }

        for (int i = 2; i < n; i++) {
            for (int j = 0; j < m-1 ; j++) {
                if (routhArray[i-1][j+1]==null)
                {   double val = routhArray[i-2][j+1] != null? routhArray[i-2][j+1]:0.0;
                    routhArray[i][j] = val;
                }
                else{
                    double val1 = routhArray[i - 1][0] != null ? routhArray[i - 1][0] : 0.0;
                    double val2 = routhArray[i - 2][j + 1] != null ? routhArray[i - 2][j + 1] : 0.0;
                    double val3 = routhArray[i - 2][0] != null ? routhArray[i - 2][0] : 0.0;
                    double val4 = routhArray[i - 1][j + 1] != null ? routhArray[i - 1][j + 1] : 0.0;

                    routhArray[i][j] = (val1 * val2 - val3 * val4) / val1;
                }
            }
            // Check if the entire row is zero
            boolean allZero = true;
            for (int j = 0; j < m; j++) {
                if (((routhArray[i][j]!= null) && (routhArray[i][j] != 0.0))  || m <= 2 ) {
                    allZero = false;
                    break;
                }
            }
            if (allZero) {
                // Replace the all-zero row with coefficients of the auxiliary equation
                int currentMaxPower = maxPower - i;
                for (int j = 0; j < m; j++) {
                    int power = currentMaxPower - 2 * j;
                    if (power >= 0) {
                        routhArray[i][j] = routhArray[i - 1][j] * (power+1);
                    } else {
                        routhArray[i][j] = 0.0;
                    }
                }
            }
            else if (routhArray[i][0]==0){
                routhArray[i][0] = 1e-9;}
        }
        return routhArray;
    }

    public static int countSignChanges(Double[][] array) {
        int signChanges = 0;

        // Check for sign changes in the first column
        int prevSign = array[0][0] >= 0 ? 1 : -1;
        for (int i = 1; i < array.length; i++) {
            int currentSign = array[i][0] >= 0 ? 1 : -1;
            if (currentSign != prevSign) {
                signChanges++;
                prevSign = currentSign;
            }
        }

        return signChanges;
    }
    public static Complex[] findRoots(double[] coefficients) {
        PolynomialFunction polynomial = new PolynomialFunction(coefficients);
        LaguerreSolver solver = new LaguerreSolver();
        return solver.solveAllComplex(polynomial.getCoefficients(), 0);
    }




}
