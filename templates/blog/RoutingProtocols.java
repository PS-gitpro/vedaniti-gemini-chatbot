import java.util.*;

public class RoutingProtocols {
    
    // Link State Routing using Dijkstra's Algorithm
    static class LinkStateRouting {
        private int[][] graph;
        private int nodes;
        
        public LinkStateRouting(int[][] adjacencyMatrix) {
            this.graph = adjacencyMatrix;
            this.nodes = adjacencyMatrix.length;
        }
        
        public void findShortestPath(int source) {
            int[] dist = new int[nodes];
            boolean[] visited = new boolean[nodes];
            int[] parent = new int[nodes];
            
            Arrays.fill(dist, Integer.MAX_VALUE);
            Arrays.fill(parent, -1);
            dist[source] = 0;
            
            for (int i = 0; i < nodes - 1; i++) {
                int u = findMinDistance(dist, visited);
                visited[u] = true;
                
                for (int v = 0; v < nodes; v++) {
                    if (!visited[v] && graph[u][v] != 0 && 
                        dist[u] != Integer.MAX_VALUE && 
                        dist[u] + graph[u][v] < dist[v]) {
                        dist[v] = dist[u] + graph[u][v];
                        parent[v] = u;
                    }
                }
            }
            
            printSolution(source, dist, parent);
        }
        
        private int findMinDistance(int[] dist, boolean[] visited) {
            int min = Integer.MAX_VALUE;
            int minIndex = -1;
            
            for (int v = 0; v < nodes; v++) {
                if (!visited[v] && dist[v] <= min) {
                    min = dist[v];
                    minIndex = v;
                }
            }
            return minIndex;
        }
        
        private void printSolution(int source, int[] dist, int[] parent) {
            System.out.println("\n=== LINK STATE ROUTING (Dijkstra) ===");
            System.out.println("Source Node: " + (char)(source + 'A'));
            System.out.println("Node\tDistance\tPath");
            
            for (int i = 0; i < nodes; i++) {
                if (i != source) {
                    System.out.print((char)(i + 'A') + "\t" + dist[i] + "\t\t");
                    printPath(i, parent);
                    System.out.println();
                }
            }
        }
        
        private void printPath(int current, int[] parent) {
            if (parent[current] == -1) {
                System.out.print((char)(current + 'A'));
                return;
            }
            printPath(parent[current], parent);
            System.out.print(" -> " + (char)(current + 'A'));
        }
    }
    
    // Distance Vector Routing using Bellman-Ford Algorithm
    static class DistanceVectorRouting {
        private int[][] graph;
        private int nodes;
        
        public DistanceVectorRouting(int[][] adjacencyMatrix) {
            this.graph = adjacencyMatrix;
            this.nodes = adjacencyMatrix.length;
        }
        
        public void findShortestPaths(int source) {
            int[] dist = new int[nodes];
            int[] parent = new int[nodes];
            
            Arrays.fill(dist, Integer.MAX_VALUE);
            Arrays.fill(parent, -1);
            dist[source] = 0;
            
            // Relax all edges n-1 times
            for (int i = 0; i < nodes - 1; i++) {
                for (int u = 0; u < nodes; u++) {
                    for (int v = 0; v < nodes; v++) {
                        if (graph[u][v] != 0 && dist[u] != Integer.MAX_VALUE && 
                            dist[u] + graph[u][v] < dist[v]) {
                            dist[v] = dist[u] + graph[u][v];
                            parent[v] = u;
                        }
                    }
                }
            }
            
            // Check for negative weight cycles
            for (int u = 0; u < nodes; u++) {
                for (int v = 0; v < nodes; v++) {
                    if (graph[u][v] != 0 && dist[u] != Integer.MAX_VALUE && 
                        dist[u] + graph[u][v] < dist[v]) {
                        System.out.println("Graph contains negative weight cycle!");
                        return;
                    }
                }
            }
            
            printSolution(source, dist, parent);
        }
        
        private void printSolution(int source, int[] dist, int[] parent) {
            System.out.println("\n=== DISTANCE VECTOR ROUTING (Bellman-Ford) ===");
            System.out.println("Source Node: " + (char)(source + 'A'));
            System.out.println("Node\tDistance\tPath");
            
            for (int i = 0; i < nodes; i++) {
                if (i != source) {
                    System.out.print((char)(i + 'A') + "\t" + dist[i] + "\t\t");
                    printPath(i, parent);
                    System.out.println();
                }
            }
        }
        
        private void printPath(int current, int[] parent) {
            if (parent[current] == -1) {
                System.out.print((char)(current + 'A'));
                return;
            }
            printPath(parent[current], parent);
            System.out.print(" -> " + (char)(current + 'A'));
        }
    }
    
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        // Sample network topology (Adjacency Matrix)
        // Nodes: A=0, B=1, C=2, D=3, E=4
        int[][] graph = {
            {0, 4, 2, 0, 0},  // A
            {4, 0, 1, 5, 0},  // B
            {2, 1, 0, 8, 10}, // C
            {0, 5, 8, 0, 2},  // D
            {0, 0, 10, 2, 0}  // E
        };
        
        System.out.println("Network Topology:");
        System.out.println("    A(0)");
        System.out.println("   / \\  ");
        System.out.println("  4   2 ");
        System.out.println(" /     \\");
        System.out.println("B(1)--C(2)");
        System.out.println("| \\   / |");
        System.out.println("5  1  10|");
        System.out.println("|   \\   |");
        System.out.println("D(3)--E(4)");
        System.out.println("   2");
        
        System.out.print("\nEnter source node (A=0, B=1, C=2, D=3, E=4): ");
        int source = scanner.nextInt();
        
        if (source < 0 || source >= graph.length) {
            System.out.println("Invalid source node!");
            return;
        }
        
        // Link State Routing
        LinkStateRouting lsr = new LinkStateRouting(graph);
        lsr.findShortestPath(source);
        
        // Distance Vector Routing
        DistanceVectorRouting dv = new DistanceVectorRouting(graph);
        dv.findShortestPaths(source);
        
        scanner.close();
    }
}