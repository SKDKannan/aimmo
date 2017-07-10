﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AvatarController : MonoBehaviour 
{
	private const float speed = 1.0f;

	private float startTime;
	private Vector3 currPosition;
	private Vector3 nextPosition;

	// Used to avoid laggy movement.
	private Queue<Vector3> positionsQueue;

	void Start()
	{
		startTime = Time.time;
		currPosition = transform.position;
		nextPosition = transform.position;
		positionsQueue = new Queue<Vector3>();
	}

	// Move the player to next position.
	void Update() 
	{
		float step = (Time.time - startTime) * speed;

		if (step < 1.0f) 
		{
			transform.position = Vector3.Lerp(currPosition, nextPosition, step);
		} 
		else 
		{
			// TODO: This won't work if the response time is longer than roughly 1 second.
			transform.position = nextPosition;
			currPosition = nextPosition;
			nextPosition = positionsQueue.Dequeue();
			startTime = Time.time;
		}
	}

	// Set next destination.
	public void SetNextPosition(Vector3 position)
	{
		positionsQueue.Enqueue(position);
	}
}
