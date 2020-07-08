#define OLC_PGE_APPLICATION
#include "olcPixelGameEngine.h"
#include <iostream>

using namespace std;

class pathFindingApp : public olc::PixelGameEngine {
public:
	pathFindingApp() {
		sAppName = "PathFinding";
	}

private:
	struct cNode {
		bool bOstacle = false;
		bool bVisited = false;
		float fGlobalGoal;
		float fLocalGoal;
		int x;
		int y;
		vector<cNode*> vecNeigbours;
		cNode* parent;
	};

	cNode* Nodes = nullptr;
	int iMapWidth = 32;
	int iMapHeight = 20;
	cNode* StartNode = nullptr;
	cNode* EndNode = nullptr;

protected:
	bool nodeSet() {
		for (int i = 0; i < iMapWidth; i++) {
			for (int j = 0; j < iMapHeight; j++) {
				Nodes[j * iMapWidth + i].x = i;
				Nodes[j * iMapWidth + i].y = j;
				Nodes[j * iMapWidth + i].bOstacle = false;
				Nodes[j * iMapWidth + i].bVisited = false;
				Nodes[j * iMapWidth + i].parent = nullptr;

			}
		}
		StartNode = &Nodes[(iMapHeight / 2 * iMapWidth)];
		EndNode = &Nodes[(iMapHeight / 2 * iMapWidth - 5)];
		return true;
	}

	void neigboursConnect() {
		for (int x = 0; x < iMapWidth; x++) {
			for (int y = 0; y < iMapHeight; y++) {
				if (x < (iMapWidth - 1))
					Nodes[y * iMapWidth + x].vecNeigbours.push_back(&Nodes[y * iMapWidth +x +1]);
				if (x > 0)
					Nodes[y * iMapWidth + x].vecNeigbours.push_back(&Nodes[y * iMapWidth + x-1]);
				if (y < (iMapHeight - 1))
					Nodes[y * iMapWidth + x].vecNeigbours.push_back(&Nodes[(y + 1) * iMapWidth + x]);
				if (y > 0)
					Nodes[y * iMapWidth + x].vecNeigbours.push_back(&Nodes[(y - 1) * iMapWidth + x]);
				if (x > 0 && y > 0)
					Nodes[y * iMapWidth + x].vecNeigbours.push_back(&Nodes[(y - 1) * iMapWidth + x - 1]);
				if (x > 0 && y < iMapHeight - 1)
					Nodes[y * iMapWidth + x].vecNeigbours.push_back(&Nodes[(y + 1) * iMapWidth + x - 1]);
				if (x < iMapWidth - 1 && y > 0)
					Nodes[y * iMapWidth + x].vecNeigbours.push_back(&Nodes[(y - 1) * iMapWidth + x + 1]);
				if (x < iMapWidth - 1 && y < iMapHeight - 1)
					Nodes[y * iMapWidth + x].vecNeigbours.push_back(&Nodes[(y + 1) * iMapWidth + x + 1]);
			}
		}
	}

	void controlKeyboard(int iNodeX, int iNodeY) {
		if (GetKey(olc::R).bHeld) {
			//reset
			for (int i = 0; i < iMapWidth; i++)
				for (int j = 0; j < iMapHeight; j++) {
					Nodes[j * iMapWidth + i].bOstacle = false;
				}
			StartNode = &Nodes[(iMapHeight / 2 * iMapWidth)];
			EndNode = &Nodes[(iMapHeight / 2 * iMapWidth - 5)];

		}

		if (GetMouse(0).bReleased || (GetMouse(0).bHeld && GetKey(olc::CTRL).bHeld)) {
			if (iNodeX >= 0 && iNodeX < iMapWidth) {
				if (iNodeY >= 0 && iNodeY < iMapHeight) {

					if (GetKey(olc::SPACE).bHeld) {
						StartNode = &Nodes[iNodeY * iMapWidth + iNodeX];
					}
					else if (GetKey(olc::SHIFT).bHeld) {
						EndNode = &Nodes[iNodeY * iMapWidth + iNodeX];
					}
					else {
						Nodes[iNodeY * iMapWidth + iNodeX].bOstacle =
							!Nodes[iNodeY * iMapWidth + iNodeX].bOstacle;
					}
				}
			}
		}
	}


	void nodeGrid(int iNodeSize, int iNodeSpace) {
		Clear(olc::BLACK);
		for (int x = 0; x < iMapWidth; x++) {
			for (int y = 0; y < iMapHeight; y++) {
				FillRect(x * iNodeSize + iNodeSpace, y * iNodeSize + iNodeSpace,
					iNodeSize - iNodeSpace, iNodeSize - iNodeSpace, olc::BLUE);

				if (&Nodes[y * iMapWidth + x] == StartNode) {
					FillRect(x * iNodeSize + iNodeSpace, y * iNodeSize + iNodeSpace,
						iNodeSize - iNodeSpace, iNodeSize - iNodeSpace, olc::GREEN);
				}
				else if (&Nodes[y * iMapWidth + x] == EndNode) {
					FillRect(x * iNodeSize + iNodeSpace, y * iNodeSize + iNodeSpace,
						iNodeSize - iNodeSpace, iNodeSize - iNodeSpace, olc::RED);
				}
				else if (Nodes[y * iMapWidth + x].bOstacle) {
					FillRect(x * iNodeSize + iNodeSpace, y * iNodeSize + iNodeSpace,
						iNodeSize - iNodeSpace, iNodeSize - iNodeSpace, olc::MAGENTA);
				}
			}
		}
	}
	
	bool astar() {
		for (int x = 0; x < iMapWidth; x++)
			for (int y = 0; y < iMapHeight; y++) {
				Nodes[y * iMapWidth + x].bVisited = false;
				Nodes[y * iMapWidth + x].fGlobalGoal = INFINITY;
				Nodes[y * iMapWidth + x].fLocalGoal = INFINITY;
				Nodes[y * iMapWidth + x].parent = nullptr;
			}

		auto distance = [](cNode* a, cNode* b) {
			return sqrtf((a->x - b->x) * (a->x - b->x) + (a->y - b->y) * (a->y - b->y));
		};

		auto heuristic = [distance](cNode* a, cNode* b) {
			return distance(a, b);
		};

		cNode* nodeCurrent = StartNode;
		StartNode->fLocalGoal = 0.0f;
		StartNode->fGlobalGoal = heuristic(StartNode, EndNode);


		list<cNode*> lNotTested;
		lNotTested.push_back(StartNode);

		while (!lNotTested.empty() && nodeCurrent != EndNode) {
			lNotTested.sort([](const cNode* lhs, const cNode* rhs) { return lhs->fGlobalGoal < rhs->fGlobalGoal; });


			while (!lNotTested.empty() && lNotTested.front()->bVisited) {
				lNotTested.pop_front();
			}

			if (lNotTested.empty()) {
				break;
			}

			nodeCurrent = lNotTested.front();
			nodeCurrent->bVisited = true;

			for (auto nodeNeighbour : nodeCurrent->vecNeigbours) {

				if (!nodeNeighbour->bVisited && nodeNeighbour->bOstacle == 0) {
					lNotTested.push_back(nodeNeighbour);
				}

				float fPossiblyLowerGoal = nodeCurrent->fLocalGoal + distance(nodeCurrent, nodeNeighbour);

				if (fPossiblyLowerGoal < nodeNeighbour->fLocalGoal) {
					nodeNeighbour->parent = nodeCurrent;
					nodeNeighbour->fLocalGoal = fPossiblyLowerGoal;
					nodeNeighbour->fGlobalGoal = nodeNeighbour->fLocalGoal + heuristic(nodeNeighbour, EndNode);
				}
			}
		}
		return true;
	}

	void pathVisual(int iNodeSize, int iNodeSpace) {
		if (EndNode != nullptr)
		{
			cNode* p = EndNode;
			while (p->parent != nullptr)
			{
				FillRect(p->x * iNodeSize + iNodeSpace, p->y * iNodeSize + iNodeSpace, iNodeSize - iNodeSpace, iNodeSize - iNodeSpace, olc::VERY_DARK_YELLOW);
				if (p->bOstacle)
					FillRect(p->x * iNodeSize + iNodeSpace, p->y * iNodeSize + iNodeSpace, iNodeSize - iNodeSpace, iNodeSize - iNodeSpace, olc::MAGENTA);
				p = p->parent;
				FillRect(EndNode->x * iNodeSize + iNodeSpace, EndNode->y * iNodeSize + iNodeSpace, iNodeSize - iNodeSpace, iNodeSize - iNodeSpace, olc::RED);

			}
		}
	}
	
	void selectPathfinding() {
		if(GetKey(olc::A).bPressed)
			astar();
	}

	virtual bool OnUserCreate() {
		Nodes = new cNode[iMapWidth * iMapHeight];
		nodeSet();
		neigboursConnect();

		return true;
	}


	virtual bool OnUserUpdate(float fElapsedTime) {
		int iNodeSize = 10;
		int iNodeSpace = 1;
		int iNodeX = GetMouseX() / iNodeSize;
		int iNodeY = GetMouseY() / iNodeSize;


		controlKeyboard(iNodeX, iNodeY);
		nodeGrid(iNodeSize, iNodeSpace);
		pathVisual(iNodeSize, iNodeSpace);
		selectPathfinding();

		return true;
	}
};


int main() {
	pathFindingApp demo;
	if (demo.Construct(300, 200, 4, 4)) {
		demo.Start();
	}
}