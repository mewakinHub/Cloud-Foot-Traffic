'use client'

import React, { useEffect, useRef, useState } from "react";

import { useSearchParams } from 'next/navigation'

export default function Dev() {
  const searchParams = useSearchParams()
  const user = searchParams.get('user')

    return (
      <>
      <div>
        <p>{user}</p>
        <p>Dev pages are created for debugging and testing purposes.</p>
      </div>
      </>
    );
  }
  